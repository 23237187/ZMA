
# from Data_Visulizor import *
#
# dv = Data_Visulizor(r"/ZTE_Demo/clusters.csv",
#                     r"/ZTE_Demo/points.csv",
#                     r"/ZTE_Demo/radius.csv",
#                     r"/ZTE_Demo/probability.csv")
# dv.read_cluster_points_and_probability()
# dv.F2_F3_draw()
# dv.F1_F2_draw()
# dv.F1_F3_draw()
# dv.draw_cluster_oval()

from src.Data_Preprocess.FCM_Visulizor import *
FCMV = FCM_Viasulizor(prob_path="/home/yang/Data_Test/sample_test/fcm/probs/part-00000",
                      point_path="/home/yang/Data_Test/sample_test/fcm/fcm_points/part-00000",
                      center_path="/home/yang/Data_Test/sample_test/fcm/centers/part-00000")
FCMV.draw_points()
# FCMV.read_center_to_df()