
from App_File_Preprocess import  *

cluster_prob_dict = {
    'Socail': 1.0 / 2.0,
    'Media': 1.0/3.0,
    'Travel': 1.0/4.0
}

cluster_2_app_dict = {
    'Socail': range(1,7),
    'Media': range(7,9),
    'Travel': range(9,13)
}

common_2_app_dict = {
    'Common':range(13, 35)
}

subsets_dict = generate_user_set_for_each_meaningful_cluster(cluster_prob_dict, 30)

# print(subsets_dict)

clusters_2_users_2_apps = clusters_2_users_2_apps_map_as_dict(cluster_2_app_dict,subsets_dict)
# print(clusters_2_users_2_apps)

common_clusters_2_users_2_apps = common_clusters_2_users_2_apps_map_as_dict(common_2_app_dict)
# print(common_clusters_2_users_2_apps)

users_list = list(range(1,31))
apps_list = list(range(1,35))

df = user_app_rating_frame_empty(users_list,apps_list)

fill_frame_for_meaningful_clusters(df, clusters_2_users_2_apps)
fill_frame_for_common_clusters(df,common_clusters_2_users_2_apps)
print(df)
# test_cluster_app_id_lists = [list(range(7)), list(range(7,9)), list(range(9, 13))]

# social_cluster_app_list = test_cluster_app_id_lists[0]
#
# social_cluster_user_app_dict = map_clustered_apps_to_clustered_users_for_one_cluster(social_cluster_app_list, subsets_list[0])
#
# print(social_cluster_user_app_dict)