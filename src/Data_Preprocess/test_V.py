__author__ = 'WinterIsComing'
from Data_Visulizor import *

dv = Data_Visulizor(r"/ZTE_Demo/clusters.csv",
                    r"/ZTE_Demo/points.csv",
                    r"/ZTE_Demo/radius.csv",
                    r"/ZTE_Demo/probability.csv")
dv.read_cluster_points_and_probability()
dv.F2_F3_draw()
dv.F1_F2_draw()
dv.F1_F3_draw()
# dv.draw_cluster_oval()