__author__ = 'root'

from src.Data_Preprocess.Results_Merge_Util import *

# Results_Merge_Util.skm_result_merge("/ZTE_Demo/SKM_Iterations", 10)
Results_Merge_Util.ratings_to_df_spark("/home/yang/Data_Test/mba/sample_next/miracle_rec/part-00000")
