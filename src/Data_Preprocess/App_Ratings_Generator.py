__author__ = 'WinterIsComing'

import os
import fileinput
import pandas as pd
from collections import Counter
import shutil
import glob
import re
import csv

class App_Ratings_Generator:
    def __init__(self, user_records_path, fpg_output_path, appid_name_map):
        self.usr_records_path = user_records_path
        self.fpg_output_path = fpg_output_path
        self.appid_name_dict = appid_name_map
        self.name_appid_dict = {k: str(v) for k, v in dict(map(reversed, self.appid_name_dict.items())).items()}
        # self.package_name_2_app_id = package_name_2_app_id
        self.usr_list = self.read_usr_list()
        self.user_date_dict = self.user_key_date_list_dict_gen()
        self.user_key_usage_dict = dict()
        self.user_key_usage_dict_gen_for_all_users()
        self.user_app_usage_frame = pd.DataFrame(self.user_key_usage_dict).T
        self.app_static_frame = self.app_static_frame_gen()
        self.user_app_usage_frame.fillna(0, inplace=True)
        self.user_app_rating_frame = self.user_app_rating_frame_gen()

    def read_usr_list(self):
        usr_list = [int(name) for name in os.listdir(self.usr_records_path)
                    if os.path.isdir(os.path.join(self.usr_records_path, str(name)))]
        return usr_list

    def user_key_date_list_dict_gen(self):
        user_days_dict = dict()
        for uid in self.usr_list:
            user_date_path = os.path.join(self.usr_records_path, str(uid))
            usr_date_list = [int(re.split('[- .]', date)[1])
                             for date in os.listdir(user_date_path)]
            usr_date_list = usr_date_list.sort()
            user_days_dict.update({uid: usr_date_list})
        return user_days_dict

    @staticmethod
    def records_file_2_app_usage_list(records_file_path):
        for line in fileinput.input(records_file_path, inplace=True):
            print(line.replace('-|-|', ','), end='')
        df = pd.read_csv(records_file_path, header=None)
        for line in fileinput.input(records_file_path, inplace=True):
            print(line.replace(',', '-|-|'), end='')
        df.columns = ['time', 'latitude', 'altitude', 'IMEI', 'package_name', 'operation_code']
        p_names_list = df.ix[:, 'package_name'].unique().tolist()
        p_names_key_time_dict = dict()
        for p_name in p_names_list:
            p_names_key_time_dict.update({p_name: 0.0})
        for p_name in p_names_list:
            tmp_frame = df.loc[df['package_name'] == p_name][['operation_code', 'time']]
            opcode_list = tmp_frame['operation_code'].tolist()
            time_list = tmp_frame['time'].tolist()
            left_cursor = 0
            state_waiting_for = 3
            for right_cursor in range(len(opcode_list)):
                if opcode_list[right_cursor] == state_waiting_for:
                    # left_cursor = right_cursor
                    if state_waiting_for == 4:
                        usage_time = time_list[right_cursor] - time_list[left_cursor]
                        if usage_time < 0.0:
                            print(usage_time)
                            print(right_cursor, left_cursor, p_name)
                            exit(-1)
                        p_names_key_time_dict[p_name] += usage_time
                        state_waiting_for = 3
                    else:  #state_waiting_for = 3:
                        state_waiting_for = 4
                left_cursor = right_cursor
        return p_names_key_time_dict

    def package_key_usage_time_dict_for_single_user(self, uid):
        path_prefix = self.usr_records_path
        user_files_path = path_prefix + '/' + str(uid)
        p_names_key_time_counter = Counter()
        filename_list = next(os.walk(user_files_path))[2]
        for filename in filename_list:
            file_path = user_files_path + '/' + filename
            p_names_key_time_dict = self.records_file_2_app_usage_list(file_path)
            p_names_key_time_dict = Counter(p_names_key_time_dict)
            p_names_key_time_counter += p_names_key_time_dict
            self.user_key_usage_dict.update({uid: dict(p_names_key_time_counter)})

    def user_key_usage_dict_gen_for_all_users(self):
        usr_list = self.usr_list
        path_prefix = self.usr_records_path
        for usr in usr_list:
            self.package_key_usage_time_dict_for_single_user(usr)

    def app_static_frame_gen(self):
        df = self.user_app_usage_frame.describe().T[['mean', 'std']]
        return df

    def user_app_rating_frame_gen(self):
        user_app_usage_frame = self.user_app_usage_frame
        user_app_rating_frame = user_app_usage_frame.copy(deep=True)
        app_static_frame = self.app_static_frame
        for user in user_app_usage_frame.index:
            for app in user_app_usage_frame.columns:
                time = user_app_usage_frame.ix[user, app]
                if time <= 0.0001:
                    continue
                mean = app_static_frame.ix[app, 'mean']
                std = app_static_frame.ix[app, 'std']
                rating = ((time - mean) / std) * 5.0 / 3.0 + 5.0
                if rating > 10.0:
                    rating = 10.0
                elif rating < 1.0:
                    rating = 1.0
                user_app_rating_frame.ix[user, app] = int(rating)
        user_app_rating_frame.fillna(0, inplace=True)
        return user_app_rating_frame


    def appid_name_convert(self, match):
        return self.name_appid_dict[match.group(0)]


    def merge_user_behavior_in_different_days(self, user_id):
        path_prefix = self.usr_records_path
        fpg_prefix = self.fpg_output_path
        user_files_path = path_prefix + '/' + str(user_id)
        outfilename = fpg_prefix + '/total_behavior_for_user_' + str(user_id) + '.txt'
        outfilename_tmp = outfilename + '_tmp'
        regex = re.compile('|'.join(re.escape(x) for x in self.name_appid_dict))
        if not os.path.exists(os.path.dirname(outfilename)):
            os.makedirs(os.path.dirname(outfilename))
        with open(outfilename_tmp, 'wb') as outfile:
            for filename in glob.glob(user_files_path + '/*.txt'):
                filename = filename.replace('\\', '/')
                with open(filename, 'rb') as readfile:
                    shutil.copyfileobj(readfile, outfile)
        with open(outfilename_tmp) as fin, open(outfilename, 'w') as fout:
            for line in fin:
                fout.write(regex.sub(self.appid_name_convert, line))
        os.remove(outfilename_tmp)

    def merge_behavir_for_users(self):
        for usr_id in self.usr_list:
            self.merge_user_behavior_in_different_days(usr_id)

    def read_uid_behavior_to_frame(self, uid):
        behavior_file_path = self.fpg_output_path + '/total_behavior_for_user_' + str(uid) + '.txt'
        for line in fileinput.input(behavior_file_path, inplace=True):
            print(line.replace('-|-|', ','), end='')
        df = pd.read_csv(behavior_file_path, header=None)
        for line in fileinput.input(behavior_file_path, inplace=True):
            print(line.replace(',', '-|-|'), end='')
        df.columns = ['time', 'latitude', 'altitude', 'IMEI', 'app_id', 'operation_code']
        df.sort(['time'], inplace=True)
        return df

    @staticmethod
    def unqify_list(list):
        seen = set()
        seen_add = seen.add
        return [x for x in list if not (x in seen or seen_add(x))]

    def timestamp_to_appid(self, df, timestamp):
        appid = df.loc[df['time'] == timestamp]['app_id'].tolist()[0]
        return appid


    def windowed_app_action_for_uid(self, df):
        behavior_frame = df
        behavior_frame = behavior_frame.loc[behavior_frame['operation_code'] == 3]
        behavior_time_list = behavior_frame['time'].tolist()
        behavior_time_list.sort()
        window_start = behavior_time_list[0]
        window_end = window_start + 30 * 60 * 1000
        records_list = [[]]
        for time_stamp in behavior_time_list[1:]:
            if time_stamp <= window_end:
                records_list[-1].append(self.timestamp_to_appid(behavior_frame, time_stamp))
            elif (time_stamp - window_end) <= 3 * 60 * 1000:
                records_list[-1].append(self.timestamp_to_appid(behavior_frame, time_stamp))
                window_end = time_stamp
            else:
                window_start = time_stamp
                window_end = window_start + 30 * 60 * 1000
                new_record_list = [self.timestamp_to_appid(behavior_frame, time_stamp)]
                records_list.append(new_record_list)
        records_list_unique = []
        for record in records_list:
            unique = self.unqify_list(record)
            records_list_unique.append(unique)

        return records_list_unique

    def combine_action_window_records_for_all_users(self):
        path_prefix = self.fpg_output_path
        usr_records_list = list()

        for usr in self.usr_list:
            behavior_frame = self.read_uid_behavior_to_frame(usr)
            usr_records = self.windowed_app_action_for_uid(behavior_frame)
            usr_records_list.append(usr_records)

        with open(path_prefix + '/transactions.txt', 'a', newline='') as output_file:
            csv_writer = csv.writer(output_file, delimiter=' ')
            for records in usr_records_list:
                csv_writer.writerows(records)

    def combine_action_window_records_for_specific_user(self, uid):
        path_prefix = self.fpg_output_path
        usr_records_list = list()


        behavior_frame = self.read_uid_behavior_to_frame(uid)
        usr_records = self.windowed_app_action_for_uid(behavior_frame)
        usr_records_list.append(usr_records)

        with open(path_prefix + '/transactions.txt', 'a', newline='') as output_file:
            csv_writer = csv.writer(output_file, delimiter=' ')
            for records in usr_records_list:
                csv_writer.writerows(records)

    def write_ratings_to_file(self):
        frame = self.user_app_rating_frame
        columns = frame.columns
        name_dict = self.name_appid_dict
        new_columns = []
        for column in columns:
            new_columns.append(name_dict[column])
        frame.columns = new_columns
        frame.to_csv(self.usr_records_path + '/ratings.csv', )

    def convert_csv_to_recommender_input(self):
        df = pd.read_csv(self.usr_records_path + '/ratings.csv')
        df = df.set_index(df.ix[:, 0])
        df.index.name = 'usr'
        df = df.ix[:, 1:]
        df = df[[str(i) for i in list(range(1, 35))]]
        list_of_records = list(df.to_records())
        elements_list = list()
        for record in list_of_records:
            record = list(record)
            uid = record[0]
            col = 0
            for value in record[1:]:
                col += 1
                elements_list.append([uid, col, value])
        with open(self.usr_records_path + "/ratings_for_als.csv", "a", newline='') as output_csv:
            csv_writer = csv.writer(output_csv, delimiter='\t')
            csv_writer.writerows(elements_list)

    @staticmethod
    def convert_csv_to_recommender_input(path):
        df = pd.read_csv(path + '/ratings.csv')
        df = df.set_index(df.ix[:, 0])
        df.index.name = 'usr'
        df = df.ix[:, 1:]
        df = df[[str(i) for i in list(range(1, 35))]]
        list_of_records = list(df.to_records())
        elements_list = list()
        for record in list_of_records:
            record = list(record)
            uid = record[0]
            col = 0
            for value in record[1:]:
                col += 1
                elements_list.append([uid, col, value])
        with open(path + "/ratings_for_als.csv", "a", newline='') as output_csv:
            csv_writer = csv.writer(output_csv, delimiter='\t')
            csv_writer.writerows(elements_list)










