__author__ = 'WinterIsComing'

from App_Ratings_Generator import *
import pprint

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


rating_generator =  App_Ratings_Generator('D:/sample_data', 'D:/fpg_data', appid_packageName_dict)
rating_generator.combine_action_window_records_for_all_users()
# rating_generator.merge_behavir_for_users()
# df = rating_generator.read_uid_behavior_to_frame(1)
# records_list = rating_generator.windowed_app_action_for_uid(df)
#
# print(records_list)

# pprint.pprint(rating_generator.user_key_usage_dict)
# print(rating_generator.user_app_rating_frame)

# App_Ratings_Generator.records_file_2_app_usage_list(records_file_path=r'D:\sample_data\30')