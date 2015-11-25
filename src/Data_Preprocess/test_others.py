__author__ = 'root'

from Results_Merge_Util import *
from src.Data_Preprocess.App_Ratings_Generator import *

# Results_Merge_Util.ratings_csv_rearange('/ZTE_Demo/sample_data/ratings.csv')
# Results_Merge_Util.recs_to_df('/ZTE_Demo/recs_2')
# App_Ratings_Generator.convert_csv_to_recommender_input("/ZTE_Demo/sample_data")
# Results_Merge_Util.merge_ratings_and_recs("/ZTE_Demo/sample_data/ratings.csv", '/ZTE_Demo/recs_2')
# Results_Merge_Util.recommendation_result_demo_process("/ZTE_Demo/sample_data/ratings.csv", "/ZTE_Demo/rec_2")
Results_Merge_Util.ratings_demo_process("/home/yang/Data_Test/mba/sample_3/miracle_rec/part-00000","/home/yang/Data_Test/mba/sample_3/after.png" )
Results_Merge_Util.ratings_demo_process("/home/yang/Data_Test/mba/sample_3/miracle_ratings/part-00000","/home/yang/Data_Test/mba/sample_3/before.png" )
# Results_Merge_Util.ratings_demo_process("/home/yang/Data_Test/mba/sample_3/miracle_ratings/part-00000")