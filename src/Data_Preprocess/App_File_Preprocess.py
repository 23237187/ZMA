__author__ = 'WinterIsComing'

import random

import pandas as pd
import numpy as np, numpy.random

import pprint

def generate_user_set_for_each_meaningful_cluster(sample_probability_dict, total_user_num):
    total_user_set = set(range(1, total_user_num + 1))
    user_subset_dict = dict()
    for cluster_name, prob in sample_probability_dict.items():
        user_subset_list = list(random.sample(total_user_set, int(total_user_num * prob)))
        user_subset_dict.update({cluster_name: user_subset_list})
    return user_subset_dict


def map_clustered_apps_to_clustered_users_for_one_cluster(app_id_list, user_id_list,
                                                          map_prob_lower_bound=0.5, map_prob_upper_bound=1.0):
    app_num = len(app_id_list)
    min_num = int(app_num * map_prob_lower_bound)
    max_num = int(app_num * map_prob_upper_bound)

    user_app_dict = dict()
    for user in user_id_list:
        len_app_list = random.sample(range(min_num, max_num + 1), 1)[0]
        app_sample_list = list(random.sample(app_id_list, len_app_list))
        user_app_dict.update({user: app_sample_list})

    return user_app_dict


def clusters_2_users_2_apps_map_as_dict(clusters_2_app_dict, clusters_2_users_dict):
    clusters_2_users_apps_map = dict()
    for cluster_name, app_list in clusters_2_app_dict.items():
        user_list = clusters_2_users_dict[cluster_name]
        user_app_dict = map_clustered_apps_to_clustered_users_for_one_cluster(app_list, user_list)
        clusters_2_users_apps_map.update({cluster_name: user_app_dict})

    return clusters_2_users_apps_map


def common_clusters_2_users_2_apps_map_as_dict(clusters_2_app_dict):
    common_clusters_2_users_apps_map = dict()
    for cluster_name, app_list in clusters_2_app_dict.items():
        user_list = range(1, 31)
        user_app_dict = map_clustered_apps_to_clustered_users_for_one_cluster(app_list, user_list,
                                                                              map_prob_lower_bound=0.0)
        common_clusters_2_users_apps_map.update({cluster_name: user_app_dict})

    return common_clusters_2_users_apps_map


def user_app_rating_frame_empty(user_list_as_index, app_list_as_col):
    df = pd.DataFrame(0, index=user_list_as_index, columns=app_list_as_col)
    return df


def truc_gauss_int(mu, sigma, buttom, top):
    smp = int(random.gauss(mu, sigma))
    while not (buttom <= smp <= top):
        smp = int(random.gauss(mu, sigma))
    return smp


def truc_gauss(mu, sigma, buttom, top):
    smp = random.gauss(mu, sigma)
    while not (buttom <= smp <= top):
        smp = random.gauss(mu, sigma)
    return smp


def truc_gauss_vector_upper(length, mu=5, sigma=5.0 / 3.0, buttom=5, top=10):
    vector = list()
    for i in range(length):
        vector.append(truc_gauss_int(mu, sigma, buttom, top))
    return vector


def truc_gauss_vector_lower(length, mu=5, sigma=5.0 / 3.0, buttom=1, top=4):
    vector = list()
    for i in range(length):
        vector.append(truc_gauss_int(mu, sigma, buttom, top))
    return vector


def truc_gauss_vector_median(length, mu=5, sigma=5.0 / 3.0, buttom=1, top=10):
    vector = list()
    for i in range(length):
        vector.append(truc_gauss_int(mu, sigma, buttom, top))
    return vector


def update_user_app_rating(df, user_id, app_id_list, rating_list):
    app_rating_dict = dict(zip(app_id_list, rating_list))
    for app_id, rating in app_rating_dict.items():
        df.set_value(user_id, app_id, rating)


def fill_frame_for_meaningful_clusters(frame, cluster_user_app_dict):
    for cluster_name, user_app_dict in cluster_user_app_dict.items():
        for usr_id, app_id_list in user_app_dict.items():
            rating_list = truc_gauss_vector_upper(len(app_id_list))
            update_user_app_rating(frame, usr_id, app_id_list, rating_list)
    return frame


def fill_frame_for_common_clusters(frame, common_user_app_dict):
    for cluster_name, user_app_dict in common_user_app_dict.items():
        for usr_id, app_id_list in user_app_dict.items():
            rating_list = truc_gauss_vector_median(len(app_id_list))
            update_user_app_rating(frame, usr_id, app_id_list, rating_list)
    return frame


def merge_two_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z


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


def generate_apps_info_for_low_freq_cluster(app_id_list):
    low_freq_apps_info_dict = dict()
    for app_id in app_id_list:
        app_info_dict = {
            'package_Name': app_id,
            'day_freq_low_bound': 1,
            'day_freq_high_bound': 6,
            'days_prob_low_bound': 0.05,
            'days_prob_high_bound': 0.25,
            'avg_time_mu': 5,
            'avg_time_sigma': 2.5
        }
        low_freq_apps_info_dict.update({app_id: app_info_dict})
    return low_freq_apps_info_dict


def generate_app_info_dict(freq_clustered_app_list_dict):
    app_info_dict = dict()
    for cluster_name, app_id_list in freq_clustered_app_list_dict.items():
        if cluster_name == 'high_freq':
            app_info_dict = merge_two_dicts(app_info_dict,
                                            generate_apps_info_for_high_freq_cluster(app_id_list))
        elif cluster_name == 'med_freq':
            app_info_dict = merge_two_dicts(app_info_dict,
                                            generate_apps_info_for_med_freq_cluster(app_id_list))
        else:
            app_info_dict = merge_two_dicts(app_info_dict,
                                            generate_apps_info_for_low_freq_cluster(app_id_list))
    return app_info_dict


def user_bahavior_in_specific_day_info(user_id, date, app_dict):
    user_bahavior_date_dict = {
        user_id: {
            date: app_dict
        }
    }




def app_usage_days_list(app_info_dict, u_app_rating):
    days_low_bound = int(app_info_dict['days_prob_low_bound'] * 20)
    days_high_bound = int(app_info_dict['days_prob_high_bound'] * 20)
    days_num = list(random.sample(range(days_low_bound, days_high_bound + 1), 1))[0]

    avg_time_mu = app_info_dict['avg_time_mu']
    avg_time_sigma = app_info_dict['avg_time_sigma']
    avg_time = avg_time_mu + (u_app_rating - 5) * avg_time_sigma
    # avg_time = truc_gauss(avg_time_mu, avg_time_sigma, 0, 120)
    if avg_time <= 0.4:
        avg_time = 0.5
    total_time = avg_time * days_num

    day_freq_low_bound = app_info_dict['day_freq_low_bound']
    day_freq_high_bound = app_info_dict['day_freq_high_bound']
    assert isinstance(days_num, int)
    freq_in_day_list = list(np.random.choice(np.arange(day_freq_low_bound, day_freq_high_bound + 1),
                                          size=days_num))

    date_list = list(random.sample(range(5, 26), days_num))
    time_distribution_on_date_list = numpy.random.dirichlet(np.ones(days_num), size=1)[0] * total_time
    time_distribution_on_date_list = time_distribution_on_date_list
    if (len(date_list) != len(time_distribution_on_date_list)):
        print('error')
        # print("len_date:%d, len_time:%d" % (len(date_list), len(time_distribution_on_date_list)))
        exit(5)
    return date_list, time_distribution_on_date_list, freq_in_day_list


def user_apps_dates_time_freq_dict(app_info_dicts, u_app_frame, user_id):
    user_apps_vector = u_app_frame.ix[user_id, :]  # pandas Series
    nonzero_app_id_list = list(user_apps_vector.index[user_apps_vector.nonzero()[0]])
    date_apps_dict = dict()
    date_freq_dict = dict()
    date_time_dict = dict()
    for app_id in nonzero_app_id_list:
        rating = user_apps_vector[app_id]
        date_list, time_distribution_list, freq_in_day_list = app_usage_days_list(app_info_dicts[app_id],
                                                                                  rating)
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


def user_date_app_bahavior_dict(bundle):
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



def generate_user_log_seed(app_info_dicts, u_app_frame):
    log_seed_dict = dict()
    for user_id in range(1, 31):
        bundle = user_apps_dates_time_freq_dict(app_info_dicts, u_app_frame, user_id)
        uid_key_behv_dict = user_date_app_bahavior_dict(bundle)
        log_seed_dict = merge_two_dicts(log_seed_dict, uid_key_behv_dict)
    return log_seed_dict






# def user_app_usage_freq_and_total_time_dict(app_info_dicts, u_app_frame, user_id, app_id):
# app_info_dict = app_info_dicts[app_id]
# days_list, days_num = app_usage_days_list(app_info_dict, u_app_frame, user_id, app_id)
# total_time = app_usage_total_time(app_info_dict, u_app_frame, user_id, app_id)
#     app_usage_dict = {app_id: app_usage_dict}
#     user_app_dict = {user_id: app_usage_dict}
#     return user_app_dict


# def split_app_daily_usage_time_in_a_mounth(app_info_dict, u_i_frame, user_id):
