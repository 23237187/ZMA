import ast
import pprint

class ResultAnalyzer:

    def __init__(self,
                 rec_list_file, after_rec_rating_file):
        self.rec_list_file = rec_list_file
        self.after_rec_rating_file = after_rec_rating_file
        self.rec_dict = self.read_recommendation_list_file()
        self.after_dict = self.read_after_rating_file()
        # pprint.pprint(self.rec_dict)
        # print("\n")
        # print("====================================================================")
        # pprint.pprint(self.after_dict)
        self.compare_two_results()



    def read_recommendation_list_file(self):
        list_file_path = self.rec_list_file
        uid_appName_rating_dict = dict()
        with open(list_file_path, 'r') as infile:
            for line in infile:
                if line.strip():
                    data_items = line.split(sep=",(")
                    item_num = len(data_items)
                    if (item_num < 1):
                        continue
                    uid = ast.literal_eval(data_items[0].replace("(", " ").strip())
                    # appid_rating_list = list()
                    for ele in data_items[1:]:
                        ele.strip().strip(')')
                        ele = ele.replace(")", " ")
                        ele = ele.replace("(", " ")
                        dict_ele = ele.split(",")
                        appName = dict_ele[0]
                        rating = float(ast.literal_eval(dict_ele[1].strip()))
                        uid_appName_rating_dict.update({(uid, appName): rating})
                    # uid_appid_rating_list.append((uid, appid_rating_list))
        return uid_appName_rating_dict

    def read_after_rating_file(self):
        file_path = self.after_rec_rating_file
        uid_appName_rating_dict = dict()
        with open(file_path, 'r') as infile:
            for line in infile:
                if line.strip():
                    line = line.replace(")", " ")
                    line = line.replace("(", " ")
                    line = line.strip()
                    dict_ele = line.split(sep=",")
                    uid = ast.literal_eval(dict_ele[0])
                    app_name = dict_ele[1]
                    rating = ast.literal_eval(dict_ele[2])
                    uid_appName_rating_dict.update({(uid, app_name): rating})
        return uid_appName_rating_dict

    def compare_two_results(self):
        rec_dict = self.rec_dict
        after_dict = self.after_dict
        wrong_dict = dict()
        correct_cnt = 0
        for k, rating_rec in rec_dict.items():
            rating_after = after_dict.get(k)
            if (rating_after >= 5.0):
                correct_cnt += 1
            else:
                wrong_dict.update({k: {"rec": rating_rec, "after": rating_after}})
        rec_length = len(list(rec_dict.items()))
        cr = correct_cnt / rec_length
        print("correct rate is: " + str(cr))
        pprint.pprint(wrong_dict)

