

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
    'high_freq': [2, 4, 7, 8, 13, 14, 23, 16, 19],
    'med_freq': [1, 3, 5, 17, 18, 20, 21, 22, 15, 24, 25],
    'low_freq': [6, 9, 10, 11, 12, 26, 27, 28, 29, 30, 31, 32, 33, 34]
}



# appid_packageName_dict = {
#     1: 'tv.danmaku.bili',
#     2: 'com.netease.cloudmusic',
#     3: 'com.youku.phone',
#     4: 'com.chaozh.iReaderFree',
#     5: 'air.tv.douyu.android',
#     6: 'me.ele',
#     7: 'com.zhihu.android',
#     8: 'com.sina.weibo',
#     9: 'com.baidu.BaiduMap',
#     10: 'com.dianping.v1',
#     11: 'com.sankuai.meituan',
#     12: 'com.gewara',
#     13: 'com.tencent.mobile.qq',
#     14: 'com.tencent.mm',
#     15: 'com.baidu.netdisk',
#     16: 'com.eg.android.AlipayGphone',
#     17: 'com.taobao.taobao',
#     18: 'com.jingdong.app.mall',
#     19: 'com.smzdm.client.android',
#     20: 'cn.ibuka.manga.ui',
#     21: 'org.qii.weiciyuan',
#     22: 'com.myzaker.ZAKER_Phone',
#     23: 'com.UCMobile',
#     24: 'com.speedsoftware.rootexplorer',
#     25: 'com.ximalaya.ting.android',
#     26: 'com.youdao.dict',
#     27: 'com.youdao.note',
#     28: 'cn.wiz.note',
#     29: 'com.sand.airdroid',
#     30: 'com.tencent.news',
#     31: 'qsbk.app',
#     32: 'com.coolapk.market',
#     33: 'com.buestc.wallet',
#     34: 'com.immomo.momo'
# }

#34之后为fake app

appid_packageName_dict = {
    1: 'tv.danmaku.bili',
    2: 'com.netease.cloudmusic',
    3: 'com.youku.phone',
    4: 'com.chaozh.iReaderFree',
    5: 'air.tv.douyu.android',
    6: 'me.ele',
    7: 'com.zhihu.android',
    8: 'com.sina.weibo',
    9: 'com.baidu.BaiduMap',
    10: 'com.dianping.v1',
    11: 'com.sankuai.meituan',
    12: 'com.gewara',
    13: 'com.tencent.mobile.qq',
    14: 'com.tencent.mm',
    15: 'com.baidu.netdisk',
    16: 'com.eg.android.AlipayGphone',
    17: 'com.taobao.taobao',
    18: 'com.jingdong.app.mall',
    19: 'com.smzdm.client.android',
    20: 'cn.ibuka.manga.ui',
    21: 'org.qii.weiciyuan',
    22: 'com.myzaker.ZAKER_Phone',
    23: 'com.UCMobile',
    24: 'com.speedsoftware.rootexplorer',
    25: 'com.ximalaya.ting.android',
    26: 'com.youdao.dict',
    27: 'com.youdao.note',
    28: 'cn.wiz.note',
    29: 'com.sand.airdroid',
    30: 'com.tencent.news',
    31: 'qsbk.app',
    32: 'com.coolapk.market',
    33: 'com.buestc.wallet',
    34: 'com.immomo.momo'
}

user_num = 500
app_num = 1000
def add_fake_app(app_dict, num=200):
    new_dict = dict()
    new_dict = app_dict
    for i in range (35, num + 1):
        fake_app_str = 'fakeApp' + str(i)
        new_dict.update({i: fake_app_str})
    return new_dict

def fake_app_dict(cluster_2_app_dict, common_2_app_dict, freq_clusered_app_list_dict, num=200):
    new_dict_1 = dict()
    new_dict = cluster_2_app_dict
    new_dict_2 = dict()
    new_dict_2 = common_2_app_dict
    new_dict_3 = dict()
    new_dict_3 = freq_clusered_app_list_dict

    total_fake_num = num - 34
    part_1_num = int(total_fake_num / 4)


    # pprint.pprint(list(range(1,7)) + list(range(35, 35 + part_1_num)))
    new_dict_1.update({'Media': list(range(1,7)) + list(range(35, 35 + part_1_num))})
    new_dict_1.update({'Social': list(range(7,9)) + list(range(35 + part_1_num, 35 + part_1_num * 2))})
    new_dict_1.update({'Travel': list(range(9,13)) + list(range(35 + part_1_num * 2, 35 + part_1_num * 3))})

    new_dict_2.update({'Common': list(range(13, 35))+ list(range(35 + part_1_num * 3, num + 1))})

    new_dict_3.update({'high_freq': [2, 4, 7, 8, 13, 14, 23, 16, 19]+ list(range(35 + part_1_num, 35 + part_1_num * 2))})
    new_dict_3.update({'med_freq': [1, 3, 5, 17, 18, 20, 21, 22, 15, 24, 25] + list(range(35, 35 + part_1_num))})
    new_dict_3.update({'low_freq': [6, 9, 10, 11, 12, 26, 27, 28, 29, 30, 31, 32, 33, 34]+ list(range(35 + part_1_num * 2, num + 1))})

    return new_dict_1, new_dict_2, new_dict_3

appid_packageName_dict = add_fake_app(appid_packageName_dict, app_num)
cluster_2_app_dict, common_2_app_dict, freq_clusered_app_list_dict = fake_app_dict(cluster_2_app_dict, common_2_app_dict, freq_clusered_app_list_dict, app_num)




# preprocessor = AppFilePreprocessor(cluster_2_app_dict, cluster_prob_dict, common_2_app_dict,
#                                     freq_clusered_app_list_dict, appid_packageName_dict)
# preprocessor.generate_log_files('/home/yang/Data_Test/sample_3')

# preprocessor = AppFilePreprocessor(cluster_2_app_dict, cluster_prob_dict, common_2_app_dict,
#                                     freq_clusered_app_list_dict, appid_packageName_dict,
#                                     seed=True,
#                                     seed_path='/home/yang/sample_2')
# preprocessor.generate_log_files('/home/yang/sample_3')

# pprint.pprint(cluster_2_app_dict)
# pprint.pprint(common_2_app_dict)
# pprint.pprint(freq_clusered_app_list_dict)

preprocessor = AppFilePreprocessor(cluster_2_app_dict, cluster_prob_dict, common_2_app_dict,
                                    freq_clusered_app_list_dict, appid_packageName_dict,
                                    seed=False,
                                    seed_path='/home/yang/Data_Test/sample_3',
                                    rec_list=False,
                                    rec_path='/home/yang/Data_Test/sample_3/miracle_rec_list/part-00000',
                                    mons=11,
                                    initial_mon=3,
                                    app_num=app_num,
                                    user_num=user_num)
preprocessor.generate_log_files('/home/yang/Data_Test/sample_huge')

# convert_csv_to_recommender_input('D:/sample_data', 'D:/sample_data')