
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
    32: 'com.coolapl.market',
    33: 'com.buestc.wallet',
    34: 'com.immomo.momo'
}


# preprocessor = AppFilePreprocessor(cluster_2_app_dict, cluster_prob_dict, common_2_app_dict,
#                                    freq_clusered_app_list_dict, appid_packageName_dict)
# preprocessor.generate_log_files('D:/sample_data')

convert_csv_to_recommender_input('D:/sample_data', 'D:/sample_data')