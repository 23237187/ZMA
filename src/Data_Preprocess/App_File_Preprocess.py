__author__ = 'WinterIsComing'

import random

import pandas as pd
import numpy as np

def generate_user_set_for_each_meaningful_cluster(sample_probability_dict, total_user_num):
    total_user_set = set(range(1, total_user_num + 1))
    user_subset_dict = dict()
    for cluster_name, prob in sample_probability_dict.items():
        user_subset_list = list(random.sample(total_user_set, int(total_user_num * prob)))
        user_subset_dict.update({cluster_name:user_subset_list})
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
        user_app_dict.update({user:app_sample_list})

    return user_app_dict

def clusters_2_users_2_apps_map_as_dict(clusters_2_app_dict,clusters_2_users_dict):
    clusters_2_users_apps_map = dict()
    for cluster_name, app_list in clusters_2_app_dict.items():
        user_list = clusters_2_users_dict[cluster_name]
        user_app_dict = map_clustered_apps_to_clustered_users_for_one_cluster(app_list, user_list)
        clusters_2_users_apps_map.update({cluster_name:user_app_dict})

    return clusters_2_users_apps_map

def common_clusters_2_users_2_apps_map_as_dict(clusters_2_app_dict):
    common_clusters_2_users_apps_map = dict()
    for cluster_name, app_list in clusters_2_app_dict.items():
        user_list = range(1,31)
        user_app_dict = map_clustered_apps_to_clustered_users_for_one_cluster(app_list, user_list,
                                                                              map_prob_lower_bound=0.0)
        common_clusters_2_users_apps_map.update({cluster_name:user_app_dict})

    return common_clusters_2_users_apps_map

def user_app_rating_frame_empty(user_list_as_index, app_list_as_col):
    df = pd.DataFrame(0, index=user_list_as_index, columns=app_list_as_col)
    return df

def truc_gauss(mu, sigma, buttom, top):
    smp = int(random.gauss(mu, sigma))
    while (buttom <= smp <= top) == False:
        smp = int(random.gauss(mu, sigma))
    return smp

def truc_gauss_vector_upper(length, mu=5, sigma=5.0/3.0, buttom=5, top=10):
    vector = list()
    for i in range(length):
        vector.append(truc_gauss(mu, sigma, buttom, top))
    return vector

def truc_gauss_vector_lower(length, mu=5, sigma=5.0/3.0, buttom=1, top=4):
    vector = list()
    for i in range(length):
        vector.append(truc_gauss(mu, sigma, buttom, top))
    return vector

def truc_gauss_vector_median(length, mu=5, sigma=5.0/3.0, buttom=1, top=10):
    vector = list()
    for i in range(length):
        vector.append(truc_gauss(mu, sigma, buttom, top))
    return vector

def update_user_app_rating(df, user_id, app_id_list, rating_list):
    app_rating_dict = dict(zip(app_id_list,rating_list))
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



