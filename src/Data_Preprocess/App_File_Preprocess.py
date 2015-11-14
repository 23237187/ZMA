__author__ = 'WinterIsComing'

import os
import sys

import random

import pandas as pd
import numpy as np, numpy.random

from datetime import datetime
from time import mktime

import collections

import pprint

import json

import fileinput
import csv
import ast
import pickle


def merge_two_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z


def convert_csv_to_recommender_input(input_path, output_path):
    df = pd.read_csv(input_path + '/ratings.csv')
    df = df.set_index(df.ix[:, 0])
    df.index.name = 'usr'
    df = df.ix[:, 1:]
    list_of_records = list(df.to_records())
    elements_list = list()
    for record in list_of_records:
        record = list(record)
        uid = record[0]
        col = 0
        for value in record[1:]:
            col += 1
            elements_list.append([uid, col, value])
    with open(output_path + "/ratings_for_als.csv", "a", newline='') as output_csv:
        csv_writer = csv.writer(output_csv, delimiter='\t')
        csv_writer.writerows(elements_list)

class AppFilePreprocessor:
    def __init__(self, special_app_clusters, special_app_clusters_prob,
                 common_app_clusters, app_freq_info,
                 appID_packageName,
                 seed=False, seed_path='',
                 rec_list=False, rec_path='',
                 mons=1,
                 initial_mon=3):

        self.cluster_appID_dict = special_app_clusters
        self.cluster_prob_dict = special_app_clusters_prob
        self.common_appID_dict = common_app_clusters
        self.freq_appIDs_dict = app_freq_info
        self.appID_packageName_dict = appID_packageName
        self.packageName_appID_dict = self.invert_appID_packageName_dict()
        # pprint.pprint(self.packageName_appID_dict)
        self.users_list = list(range(1, 31))
        self.apps_list = list(range(1, 35))
        self.seed = seed
        self.seed_path = seed_path
        self.rec_list = rec_list
        self.rec_path = rec_path
        self.mons = mons
        self.initial_mon = initial_mon

        if self.seed == False :
            self.user_subset_for_specail_cluster_dict = self.generate_user_set_for_each_meaningful_cluster()
            self.special_clusters_users_apps_dict = self.clusters_2_users_2_apps_map_as_dict()
            self.common_cluster_users_apps_dict = self.common_clusters_2_users_2_apps_map_as_dict()
        else:
            self.special_clusters_users_apps_dict = self.load_spec_cluster_dist_file()
            self.common_cluster_users_apps_dict = self.load_common_cluster_dist_file()
        self.user_app_rating_frame = self.user_app_rating_frame_empty()
        self.user_app_rating_frame = self.fill_frame_for_meaningful_clusters()
        self.user_app_rating_frame = self.fill_frame_for_common_clusters()
        if self.rec_list == True:
            self.merge_recList_2_rating_frame()
        self.app_info_dict = self.generate_app_info_dict()
        self.mon_log_seed_list = self.generate_mons_log_seed()


    def load_spec_cluster_dist_file(self, suffix='/cluster_dist_spec.txt'):
        spec_dict = dict()
        with open(self.seed_path + suffix, 'r') as spec_file:
            spec_dict = json.load(spec_file)
            # pprint.pprint(spec_dict, width=1)
        return spec_dict

    def load_common_cluster_dist_file(self, suffix='/cluster_dist_common.txt'):
        common_dict = dict()
        with open(self.seed_path + suffix, 'r') as common_file:
            common_dict = json.load(common_file)
            # pprint.pprint(common_dict, width=1)
        return common_dict

    def generate_user_set_for_each_meaningful_cluster(self, total_user_num=30):
        total_user_set = set(range(1, total_user_num + 1))
        user_subset_dict = dict()
        for cluster_name, prob in self.cluster_prob_dict.items():
            user_subset_list = list(random.sample(total_user_set, int(total_user_num * prob)))
            user_subset_dict.update({cluster_name: user_subset_list})
        return user_subset_dict


    @staticmethod
    def map_clustered_apps_to_clustered_users_for_one_cluster(app_id_list, user_id_list,
                                                              map_prob_lower_bound=0.0, map_prob_upper_bound=1.0):
        app_num = len(app_id_list)
        min_num = int(app_num * map_prob_lower_bound)
        max_num = int(app_num * map_prob_upper_bound)

        user_app_dict = dict()
        for user in user_id_list:
            len_app_list = random.sample(range(min_num, max_num + 1), 1)[0]
            app_sample_list = list(random.sample(app_id_list, len_app_list))
            user_app_dict.update({user: app_sample_list})

        return user_app_dict


    def clusters_2_users_2_apps_map_as_dict(self):
        clusters_2_app_dict = self.cluster_appID_dict
        clusters_2_users_dict = self.user_subset_for_specail_cluster_dict
        clusters_2_users_apps_map = dict()
        for cluster_name, app_list in clusters_2_app_dict.items():
            user_list = clusters_2_users_dict[cluster_name]
            user_app_dict = self.map_clustered_apps_to_clustered_users_for_one_cluster(app_list, user_list)
            clusters_2_users_apps_map.update({cluster_name: user_app_dict})

        return clusters_2_users_apps_map


    def common_clusters_2_users_2_apps_map_as_dict(self):
        clusters_2_app_dict = self.common_appID_dict
        common_clusters_2_users_apps_map = dict()
        for cluster_name, app_list in clusters_2_app_dict.items():
            user_list = range(1, 31)
            user_app_dict = self.map_clustered_apps_to_clustered_users_for_one_cluster(app_list, user_list,
                                                                                       map_prob_lower_bound=0.5)
            common_clusters_2_users_apps_map.update({cluster_name: user_app_dict})

        return common_clusters_2_users_apps_map


    def user_app_rating_frame_empty(self):
        user_list_as_index = self.users_list
        app_list_as_col = self.apps_list
        df = pd.DataFrame(0, index=user_list_as_index, columns=app_list_as_col)
        return df


    @staticmethod
    def truc_gauss_int(mu, sigma, buttom, top):
        smp = int(random.gauss(mu, sigma))
        while not (buttom <= smp <= top):
            smp = int(random.gauss(mu, sigma))
        return smp


    @staticmethod
    def truc_gauss(mu, sigma, buttom, top):
        smp = random.gauss(mu, sigma)
        while not (buttom <= smp <= top):
            smp = random.gauss(mu, sigma)
        return smp


    def truc_gauss_vector_upper(self, length, mu=5, sigma=5.0 / 3.0, buttom=5, top=10):
        vector = list()
        for i in range(length):
            vector.append(self.truc_gauss_int(mu, sigma, buttom, top))
        return vector


    def truc_gauss_vector_lower(self, length, mu=5, sigma=5.0 / 3.0, buttom=1, top=4):
        vector = list()
        for i in range(length):
            vector.append(self.truc_gauss_int(mu, sigma, buttom, top))
        return vector


    def truc_gauss_vector_median(self, length, mu=5, sigma=5.0 / 3.0, buttom=1, top=10):
        vector = list()
        for i in range(length):
            vector.append(self.truc_gauss_int(mu, sigma, buttom, top))
        return vector

    @staticmethod
    def update_user_app_rating(df, user_id, app_id_list, rating_list):
        app_rating_dict = dict(zip(app_id_list, rating_list))
        for app_id, rating in app_rating_dict.items():
            df.set_value(user_id, app_id, rating)
        # print(df)
        if df.ix[user_id, 13] < 1.0:
            qq_rating = random.sample(range(4, 7), 1)[0]
            df.set_value(user_id, 13, qq_rating)
        if df.ix[user_id, 14] < 1.0:
            wx_rating = random.sample(range(4, 7), 1)[0]
            df.set_value(user_id, 14, wx_rating)


    def fill_frame_for_meaningful_clusters(self):
        frame = self.user_app_rating_frame
        cluster_user_app_dict = self.special_clusters_users_apps_dict
        if self.seed == False:
            for cluster_name, user_app_dict in cluster_user_app_dict.items():
                for usr_id, app_id_list in user_app_dict.items():
                    rating_list = self.truc_gauss_vector_upper(len(app_id_list))
                    self.update_user_app_rating(frame, usr_id, app_id_list, rating_list)
            return frame
        else:
            for cluster_name, user_app_dict in cluster_user_app_dict.items():
                for usr_id, app_id_list in user_app_dict.items():
                    usr_id = int(usr_id)
                    rating_list = self.truc_gauss_vector_upper(len(app_id_list))
                    self.update_user_app_rating(frame, usr_id, app_id_list, rating_list)
            return frame


    def fill_frame_for_common_clusters(self):
        frame = self.user_app_rating_frame
        common_user_app_dict = self.common_cluster_users_apps_dict
        if self.seed == False:
            for cluster_name, user_app_dict in common_user_app_dict.items():
                for usr_id, app_id_list in user_app_dict.items():
                    rating_list = self.truc_gauss_vector_median(len(app_id_list))
                    self.update_user_app_rating(frame, usr_id, app_id_list, rating_list)
            return frame
        else:
            for cluster_name, user_app_dict in common_user_app_dict.items():
                for usr_id, app_id_list in user_app_dict.items():
                    usr_id = int(usr_id)
                    rating_list = self.truc_gauss_vector_median(len(app_id_list))
                    self.update_user_app_rating(frame, usr_id, app_id_list, rating_list)
            return frame

    def merge_recList_2_rating_frame(self):
        uid_appid_rating_list = self.read_recommendation_list_file()
        self.modify_rating_frame_element(self.user_app_rating_frame, uid_appid_rating_list)

    @staticmethod
    def modify_rating_frame_element(df, uid_appid_rating_list):
        for uid, appid_rating_list in uid_appid_rating_list:
            for appid, rating in appid_rating_list:
                df.set_value(uid, appid, rating)

    def invert_appID_packageName_dict(self):
        return { v: k for k, v in self.appID_packageName_dict.items()}


    def read_recommendation_list_file(self):
        list_file_path = self.rec_path
        uid_appid_rating_list = list()
        with open(list_file_path, 'r') as infile:
            for line in infile:
                if line.strip():
                    data_items = line.split(sep=",(")
                    item_num = len(data_items)
                    if (item_num < 1):
                        continue
                    uid = ast.literal_eval(data_items[0].replace("(", " ").strip())
                    appid_rating_list = list()
                    for ele in data_items[1:]:
                        ele.strip().strip(')')
                        ele = ele.replace(")", " ")
                        ele = ele.replace("(", " ")
                        dict_ele = ele.split(",")
                        appID = self.packageName_appID_dict[dict_ele[0]]
                        # rating = int(ast.literal_eval(dict_ele[1].strip())) + 1
                        rating = 10.0
                        appid_rating_list.append((appID, rating))
                    uid_appid_rating_list.append((uid, appid_rating_list))
        return uid_appid_rating_list



    @staticmethod
    def generate_apps_info_for_high_freq_cluster(app_id_list):
        high_freq_apps_info_dict = dict()
        for app_id in app_id_list:
            app_info_dict = {
                'package_Name': app_id,
                'day_freq_low_bound': 10,
                'day_freq_high_bound': 35,
                'days_prob_low_bound': 0.75,
                'days_prob_high_bound': 1.00,
                'avg_time_mu': 30,
                'avg_time_sigma': 10
            }
            high_freq_apps_info_dict.update({app_id: app_info_dict})
        return high_freq_apps_info_dict


    @staticmethod
    def generate_apps_info_for_med_freq_cluster(app_id_list):
        med_freq_apps_info_dict = dict()
        for app_id in app_id_list:
            app_info_dict = {
                'package_Name': app_id,
                'day_freq_low_bound': 7,
                'day_freq_high_bound': 15,
                'days_prob_low_bound': 0.50,
                'days_prob_high_bound': 0.75,
                'avg_time_mu': 30,
                'avg_time_sigma': 10
            }
            med_freq_apps_info_dict.update({app_id: app_info_dict})
        return med_freq_apps_info_dict


    @staticmethod
    def generate_apps_info_for_low_freq_cluster(app_id_list):
        low_freq_apps_info_dict = dict()
        for app_id in app_id_list:
            app_info_dict = {
                'package_Name': app_id,
                'day_freq_low_bound': 1,
                'day_freq_high_bound': 6,
                'days_prob_low_bound': 0.2,
                'days_prob_high_bound': 0.25,
                'avg_time_mu': 5,
                'avg_time_sigma': 2.5
            }
            low_freq_apps_info_dict.update({app_id: app_info_dict})
        return low_freq_apps_info_dict


    def generate_app_info_dict(self):
        freq_clustered_app_list_dict = self.freq_appIDs_dict
        app_info_dict = dict()
        for cluster_name, app_id_list in freq_clustered_app_list_dict.items():
            if cluster_name == 'high_freq':
                app_info_dict = merge_two_dicts(app_info_dict,
                                                self.generate_apps_info_for_high_freq_cluster(app_id_list))
            elif cluster_name == 'med_freq':
                app_info_dict = merge_two_dicts(app_info_dict,
                                                self.generate_apps_info_for_med_freq_cluster(app_id_list))
            else:
                app_info_dict = merge_two_dicts(app_info_dict,
                                                self.generate_apps_info_for_low_freq_cluster(app_id_list))
        return app_info_dict


    def app_usage_days_list(self, app_info_dict, u_app_rating, sample_days_list):
        days_how_many = len(sample_days_list)
        days_low_bound = int(app_info_dict['days_prob_low_bound'] * days_how_many)#change needed
        days_high_bound = int(app_info_dict['days_prob_high_bound'] * days_how_many)#change needed
        days_num = list(random.sample(range(days_low_bound, days_high_bound + 1), 1))[0]

        avg_time_mu = app_info_dict['avg_time_mu']
        avg_time_sigma = app_info_dict['avg_time_sigma']
        avg_time = avg_time_mu + (u_app_rating - 5) * avg_time_sigma
        # avg_time = truc_gauss(avg_time_mu, avg_time_sigma, 0, 120)
        if avg_time <= 0.4 * 60:
            avg_time = 0.5 * 60 #单位 小时 =》 分钟
        total_time = avg_time * days_num

        day_freq_low_bound = app_info_dict['day_freq_low_bound']
        day_freq_high_bound = app_info_dict['day_freq_high_bound']
        assert isinstance(days_num, int)
        freq_in_day_list = list(np.random.choice(np.arange(day_freq_low_bound, day_freq_high_bound + 1),
                                                 size=days_num))
        date_list = list(random.sample(sample_days_list, days_num))
        #change needed
        time_distribution_on_date_list = numpy.random.dirichlet(np.ones(days_num), size=1)[0] * total_time
        if (len(date_list) != len(time_distribution_on_date_list)):
            print('error')
            # print("len_date:%d, len_time:%d" % (len(date_list), len(time_distribution_on_date_list)))
            exit(5)
        return date_list, time_distribution_on_date_list, freq_in_day_list


    def user_apps_dates_time_freq_dict(self, user_id, sample_days_list):
        app_info_dicts = self.app_info_dict
        u_app_frame = self.user_app_rating_frame
        user_apps_vector = u_app_frame.ix[user_id, :]  # pandas Series
        nonzero_app_id_list = list(user_apps_vector.index[user_apps_vector.nonzero()[0]])
        date_apps_dict = dict()
        date_freq_dict = dict()
        date_time_dict = dict()
        for app_id in nonzero_app_id_list:
            rating = user_apps_vector[app_id]
            date_list, time_distribution_list, freq_in_day_list = self.app_usage_days_list(app_info_dicts[app_id],
                                                                                           rating,
                                                                                           sample_days_list)
            date_freq_dict_tmp = dict(zip(date_list, freq_in_day_list))
            date_time_dict_tmp = dict(zip(date_list, time_distribution_list))

            ones = np.ones(len(date_list), dtype=int).tolist()
            date_1_hot_series = dict(zip(date_list, ones))

            date_apps_dict.update({app_id: date_1_hot_series})
            date_freq_dict.update({app_id: date_freq_dict_tmp})
            date_time_dict.update({app_id: date_time_dict_tmp})

            # user_apps_dict.update({app_id, time_dict})

        # user_apps_dict = {user_id: user_apps_dict}
        # df = pd.DataFrame(date_apps_dict)
        user_date_app = {user_id: date_apps_dict}
        user_date_freq = {user_id: date_freq_dict}
        user_date_time = {user_id: date_time_dict}
        uda_bundle_dict = {
            'user_date_app_dict': user_date_app,
            'user_date_freq_dict': user_date_freq,
            'user_date_time_dict': user_date_time
        }
        return uda_bundle_dict


    def user_date_app_bahavior_dict(self, bundle):
        # print(list(bundle['user_date_app_dict'].items())[0])
        user_id, date_apps_dict = list(bundle['user_date_app_dict'].items())[0]
        date_freq_dict = bundle['user_date_freq_dict'][user_id]
        # pprint.pprint(date_freq_dict, width=1)
        date_time_dict = bundle['user_date_time_dict'][user_id]

        df = pd.DataFrame(date_apps_dict).fillna(0)
        # print(df)
        dates = df.index.tolist()

        date_behavior_dict = dict()
        for date in dates:
            apps = df.columns[df.ix[date].nonzero()].tolist()
            # print(apps)
            # print(df.ix[date])
            # print(df.ix[date].nonzero())
            apps_behavior_dict = dict()
            for app_id in apps:
                # print("%d, %d" % (date, app_id))
                # pprint.pprint(date_time_dict, width=1)
                behavior_dict = {
                    'freq': date_freq_dict[app_id][date],
                    'time': date_time_dict[app_id][date]
                }
                apps_behavior_dict.update({app_id: behavior_dict})
            date_behavior_dict.update({date: apps_behavior_dict})

        uid_key_date_behavior_dict = {user_id: date_behavior_dict}
        return uid_key_date_behavior_dict


    def generate_mons_log_seed(self):
        month_num = self.mons
        monthNo_log_seed_list = list()
        if self.initial_mon != 3:
            ini_cnt = 2
        else:
            ini_cnt = 1
        for cnt in range(ini_cnt, month_num + 1):
            month_idx = cnt + 2
            if (cnt == 1):
                sample_day_num = 20
                sample_days_list = list(range(5, 26))
            else:
                sample_day_num = list(random.sample(range(15, 21), 1))[0]
                sample_days_list = list(random.sample(range(1, 30), sample_day_num))
            log_seed_dict = self.generate_user_log_seed(sample_days_list)
            monthNo_log_seed_list.append((month_idx, log_seed_dict))
        return monthNo_log_seed_list

    def generate_user_log_seed(self, sample_days_list):
        log_seed_dict = dict()
        for user_id in range(1, 31):
            bundle = self.user_apps_dates_time_freq_dict(user_id, sample_days_list)
            uid_key_behv_dict = self.user_date_app_bahavior_dict(bundle)
            log_seed_dict = merge_two_dicts(log_seed_dict, uid_key_behv_dict)
        return log_seed_dict


    def generate_start_end_timestamps(self, mon_idx, date, freq, time):
        time_distribution_list = numpy.random.dirichlet(np.ones(freq), size=1)[0] * time * 60.0
        start_time = int(mktime(datetime(2015 + int(mon_idx / 12), int(mon_idx) % 12, date, 8, 0).timetuple()))
        #change needed
        end_time = int(mktime(datetime(2015 + int(mon_idx / 12), int(mon_idx) % 12, date, 23, 59).timetuple()))
        #change needed
        start_time_list = list(random.sample(range(start_time, end_time), freq))
        start_end_list = list()
        for start_point, duration in dict(zip(start_time_list, time_distribution_list)).items():
            start_point = start_point * 1000 + list(random.sample(range(0, 1000), 1))[0]
            end_point = start_point + duration * 1000.0
            start_end_list.append({'start': start_point, 'end': end_point})
        start_end_list.sort(key=lambda x: x['start'])
        # start_end_dict_sorted_by_start = collections.OrderedDict(sorted(start_end_dict.items(), key=lambda t:t[0]))
        return start_end_list


    # def map_uid_2_imei(self, uid):
    #     imei = self.uid_IMEI_dict[uid]
    #     return imei


    def map_appid_2_packageName(self, appID):
        packageName = self.appID_packageName_dict[appID]
        return packageName


    def record_dict(self, user_id, app_id, time_pair):
        s_dict = {
            'time': int(time_pair['start']),
            'latitude': 'null',
            'altitude': 'null',
            'IMEI': user_id,
            'package_name': self.map_appid_2_packageName(app_id),
            'operation_code': 3
        }
        e_dict = {
            'time': int(time_pair['end']),
            'latitude': 'null',
            'altitude': 'null',
            'IMEI': user_id,
            'package_name': self.map_appid_2_packageName(app_id),
            'operation_code': 4
        }
        return s_dict, e_dict


    def generate_log_file_for_user_date(self, user_id, mon_idx, date, app_key_behav_dict, path_prefix):
        app_key_start_end_dict = dict()
        for app_id, behav_dict in app_key_behav_dict.items():
            start_end_list = self.generate_start_end_timestamps(mon_idx, date, behav_dict['freq'], behav_dict['time'])
            app_key_start_end_dict.update({app_id: start_end_list})

        record_list = list()
        for app_id, start_end_list in app_key_start_end_dict.items():
            for time_pair in start_end_list:
                s_dict, e_dict = self.record_dict(user_id, app_id, time_pair)
                record_list.append(s_dict)
                record_list.append(e_dict)
        record_frame = pd.DataFrame(record_list)

        record_frame.sort(['time'], inplace=True)
        record_frame = record_frame.reindex_axis(
            ['time', 'latitude', 'altitude', 'IMEI', 'package_name', 'operation_code'],
            axis=1)

        # print(record_frame)
        month_str = str(mon_idx)
        filename = path_prefix + '/' + month_str + '-' + str(date) + '.txt'
        record_frame.to_csv(filename, header=False, index=False)
        for line in fileinput.input(filename, inplace=True):
            print(line.replace(',', '-|-|'), end='')


    def generate_log_files_for_user(self, user_id, mon_idx, date_key_behav_dict, path_prefix):
        user_folder_path = path_prefix + '/' + str(user_id)
        os.makedirs(user_folder_path, exist_ok=True)
        os.chdir(user_folder_path)
        for date, app_key_behav_dict in date_key_behav_dict.items():
            self.generate_log_file_for_user_date(user_id, mon_idx, date, app_key_behav_dict, user_folder_path)


    def generate_log_files(self, files_path):
        mon_log_seed_list = self.mon_log_seed_list
        os.makedirs(files_path, exist_ok=True)
        self.user_app_rating_frame.to_csv(files_path + '/ratings.csv')
        with open(files_path + '/cluster_dist_spec.txt', 'w') as spec_file:
            json.dump(self.special_clusters_users_apps_dict, spec_file)
        with open(files_path + '/cluster_dist_common.txt', 'w') as common_file:
            json.dump(self.common_cluster_users_apps_dict, common_file)
        with open(files_path + '/mon_log_seed.txt', 'wb') as seed_file:
            pickle.dump(self.mon_log_seed_list, seed_file)
        for mon_idx, log_seed_dict in mon_log_seed_list:
            for user, date_key_behav_dict in log_seed_dict.items():
                self.generate_log_files_for_user(user, mon_idx, date_key_behav_dict, files_path)


