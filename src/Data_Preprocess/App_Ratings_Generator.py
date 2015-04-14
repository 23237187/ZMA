__author__ = 'WinterIsComing'

import os
import re

class App_Ratings_Generator:
    def __init__(self, user_records_path, package_name_2_app_id):
        self.usr_records_path = user_records_path
        self.package_name_2_app_id = package_name_2_app_id
        self.usr_list = self.read_usr_list()
        self.user_date_dict = self.user_key_date_list_dict_gen()

    def read_usr_list(self):
        usr_list = [int(name) for name in os.listdir(self.usr_records_path)
                    if os.path.isdir(name)]
        return usr_list

    def user_key_date_list_dict_gen(self):
        user_days_dict = dict()
        for uid in self.usr_list:
            user_date_path = os.path.join(self.usr_records_path, uid)
            usr_date_list = [int(re.split('[- .]', date)[1])
                             for date in os.listdir(user_date_path)]
            usr_date_list = usr_date_list.sort()
            user_days_dict.update({uid: usr_date_list})
        return user_days_dict

    def records_file_2_app_usage_list(self, records_file_path):
        with open()


