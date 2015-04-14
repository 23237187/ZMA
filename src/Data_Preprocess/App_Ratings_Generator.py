__author__ = 'WinterIsComing'

import os
import re
import fileinput
import pandas as pd
from collections import Counter

class App_Ratings_Generator:
    def __init__(self, user_records_path):
        self.usr_records_path = user_records_path
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










