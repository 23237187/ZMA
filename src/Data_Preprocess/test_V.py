__author__ = 'WinterIsComing'
from Data_Visulizor import *

dv = Data_Visulizor(r"D:\ZTE_Demo\clusters.csv",
                    r"D:\ZTE_Demo\points.csv",
                    r"D:\ZTE_Demo\radius.csv",
                    r"D:\ZTE_Demo\probability.csv")
dv.read_cluster_points_and_probability()
dv.F2_F3_draw()
# dv.draw_cluster_oval()