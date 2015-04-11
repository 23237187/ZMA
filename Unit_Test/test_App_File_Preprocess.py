
from App_File_Preprocess import  *
import pprint

cluster_prob_dict = {
    'Media': 1.0 / 2.0,
    'Social': 1.0/3.0,
    'Travel': 1.0/4.0
}

cluster_2_app_dict = {
    'Media': range(1,7),
    'Social': range(7,9),
    'Travel': range(9,13)
}

common_2_app_dict = {
    'Common':range(13, 35)
}

# # app信息字典:APP_ID,package_Name,day_freq_low_bound, day_freq_high_bound,
# app_info_dict = {
#     1: {
#         'package_Name': 1,
#         'day_freq_low_bound': 10,
#         'day_freq_high_bound': 35,
#         'days_prob_low_bound': 0.75,
#         'days_prob_high_bound': 1.00,
#         'avg_time_mu': 30
#         'avg_time_sigma': 10
#     },
#
#
# }

freq_clusered_app_list_dict = {
    'high_freq': [2, 4, 7, 8, 13, 14, 15, 16, 17, 18],
    'med_freq': [1, 3, 5, 19, 20, 21, 22, 23, 24, 25],
    'low_freq': [6, 9, 10, 11, 12, 26, 27, 28, 29, 30, 31, 32, 33, 34]
}

app_info_dict = generate_app_info_dict(freq_clusered_app_list_dict)
pprint.pprint(app_info_dict, width=1)
# print(app_info_dict)

subsets_dict = generate_user_set_for_each_meaningful_cluster(cluster_prob_dict, 30)
#
# # print(subsets_dict)
#
clusters_2_users_2_apps = clusters_2_users_2_apps_map_as_dict(cluster_2_app_dict,subsets_dict)
# # print(clusters_2_users_2_apps)
#
common_clusters_2_users_2_apps = common_clusters_2_users_2_apps_map_as_dict(common_2_app_dict)
# # print(common_clusters_2_users_2_apps)
#
users_list = list(range(1,31))
apps_list = list(range(1,35))
#
df = user_app_rating_frame_empty(users_list,apps_list)
#
fill_frame_for_meaningful_clusters(df, clusters_2_users_2_apps)
fill_frame_for_common_clusters(df,common_clusters_2_users_2_apps)
# print(df)

one_hot_date = user_apps_dates_time_freq_dict(app_info_dict, df, 5)
print(one_hot_date)
# test_cluster_app_id_lists = [list(range(7)), list(range(7,9)), list(range(9, 13))]

# social_cluster_app_list = test_cluster_app_id_lists[0]
#
# social_cluster_user_app_dict = map_clustered_apps_to_clustered_users_for_one_cluster(social_cluster_app_list, subsets_list[0])
#
# print(social_cluster_user_app_dict)