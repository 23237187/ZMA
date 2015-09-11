__author__ = 'root'

from App_Ratings_Generator import *
from Results_Merge_Util import *
from FPG_Processor import *
import sys

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

# for linux demo run
if __name__ == "__main__":
    if sys.argv[3] == "tran_gen":
        rating_generator = App_Ratings_Generator(sys.argv[1], sys.argv[2], appid_packageName_dict)
        rating_generator.merge_behavir_for_users()
        rating_generator.combine_action_window_records_for_all_users()
    elif sys.argv[3] == "rule_gen":
        Results_Merge_Util.fpg_result_merge("/ZTE_Demo/FPG_result")
        fpg = FPG_Processor("/ZTE_Demo/FPG_result/result.txt", "/ZTE_Demo/FPG_result/fpg_result.txt")
        fpg.run_generate_rule()

# for test
# fpg = FPG_Processor("/RESULT/FPG_result/result.txt", "/RESULT/FPG_result/fpg_result.txt")
# # fpg.run_generate_rule()
# fpg.fpg_result_demo_process()


