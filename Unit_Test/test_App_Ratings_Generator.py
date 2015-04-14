__author__ = 'WinterIsComing'

from App_Ratings_Generator import *
import pprint



rating_generator =  App_Ratings_Generator('D:/sample_data')
# pprint.pprint(rating_generator.user_key_usage_dict)
print(rating_generator.user_app_rating_frame)

# App_Ratings_Generator.records_file_2_app_usage_list(records_file_path=r'D:\sample_data\30')