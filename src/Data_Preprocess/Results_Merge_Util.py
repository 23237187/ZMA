__author__ = 'root'

import pandas as pd
import numpy as np
import ast
import glob
import fileinput
import pprint
import seaborn as sns


class Results_Merge_Util:
    @staticmethod
    def convert_skm_centroid_to_df(raw_centroid_file):
        lines = raw_centroid_file.readlines()[2: 5]
        weight_key_centroid_dict = dict()
        weight_list = list()
        sorted_centroid_list = list()
        for line in lines:
            segments = line.strip().split("=")
            weight = ast.literal_eval(segments[2].strip().split(',')[0])
            weight_list.append(weight)
            centroid_vec = ast.literal_eval(segments[-1].strip())
            weight_key_centroid_dict.update({weight: centroid_vec})
        weight_list.sort()
        for w in weight_list:
            cv = weight_key_centroid_dict[w]
            sorted_centroid_list.append(cv)
        df = pd.DataFrame(sorted_centroid_list)

        return df


    @staticmethod
    def skm_result_merge(file_path, iter_num):
        with open(file_path + "/SKM-1") as file:
            centroid_frame = Results_Merge_Util.convert_skm_centroid_to_df(file)
        for i in range(2, iter_num + 1):
            with open(file_path + "/SKM-" + str(i)) as file:
                centroid_frame += Results_Merge_Util.convert_skm_centroid_to_df(file)
        centroid_frame = centroid_frame.div(10)
        centroid_frame.to_csv(file_path + "/centroids.csv", header=None)

    @staticmethod
    def fpg_result_merge(file_path):
        read_files = glob.glob(file_path + "/part-*")
        with open(file_path + "/result.txt", "wb") as outfile:
            for f in read_files:
                with open(f, "rb") as infile:
                    outfile.write(infile.read())

        for line in fileinput.input(file_path + "/result.txt", inplace=True):
            print(line.replace(")", ""), end='')
        for line in fileinput.input(file_path + "/result.txt", inplace=True):
            print(line.replace("(", ""), end='')

    @staticmethod
    def ratings_csv_rearange(file_path):
        df = pd.read_csv(file_path)
        df = df.set_index(df.ix[:, 0])
        df.index.name = 'usr'
        df = df.ix[:, 1:]
        df = df[[str(i) for i in list(range(1, 35))]]
        # print(df)
        return df

    @staticmethod
    def recs_to_df(file_path):
        for line in fileinput.input(file_path, inplace=True):
            if fileinput.isfirstline():
               line = line.replace("1\t", "{1\t")
            print(line, end='')
        for line in fileinput.input(file_path, inplace=True):
            print(line.replace("[", ":{"), end='')
        for line in fileinput.input(file_path, inplace=True):
            print(line.replace("]", "},"), end='')
        with open(file_path, 'a') as file:
            file.write("}")
        with open(file_path) as file:
            content = file.read()
            recs_dict = ast.literal_eval(content)
        df = pd.DataFrame.from_dict(recs_dict).fillna(0)
        df = df.T
        df.index.name = 'usr'
        df.columns = [str(i) for i in df.columns]
        # print(df)
        return df

    @staticmethod
    def ratings_to_df_spark(file_path):
        out_path = file_path + "_2"
        with open(out_path, "w") as out_file:
            with open(file_path, "r") as in_file:
                out_file.write(in_file.read())

        for line in fileinput.input(out_path, inplace=True):
            print(line.replace("(", ""), end='')
        for line in fileinput.input(out_path, inplace=True):
            print(line.replace(")", ""), end='')

        uid_appName_rating_dict = dict()
        with open(out_path, 'r') as infile:
            for line in infile:
                dict_ele = line.split(sep=",")
                uid = ast.literal_eval(dict_ele[0])
                app_name = dict_ele[1]
                rating = ast.literal_eval(dict_ele[2])
                if uid not in uid_appName_rating_dict.keys():
                    tmp = dict()
                    tmp.setdefault(app_name, rating)
                    uid_appName_rating_dict.setdefault(uid, tmp)
                else:
                    tmp = uid_appName_rating_dict.get(uid)
                    tmp = tmp.setdefault(app_name, rating)
                    uid_appName_rating_dict.setdefault(uid, tmp)

        df = pd.DataFrame.from_dict(uid_appName_rating_dict).fillna(0)
        df = df.T
        df.index.name = 'usr'

        print(df)
        return df

    @staticmethod
    def merge_ratings_and_recs(ratings_path, recs_path):
        ratings = Results_Merge_Util.ratings_csv_rearange(ratings_path)
        recs = Results_Merge_Util.recs_to_df(recs_path)
        df = ratings.add(recs, fill_value=0)
        df = df[[str(i) for i in list(range(1, 35))]]
        return df

    @staticmethod
    def recommendation_result_demo_process(ratings_path, recs_path):
        fill_df = Results_Merge_Util.merge_ratings_and_recs(ratings_path, recs_path)
        sns.set()
        sns.heatmap(fill_df)
        sns.plt.show()

    # @staticmethod
    # def ratings_demo_process(ratings_path):
    #     df = Results_Merge_Util.ratings_csv_rearange(ratings_path)
    #     sns.set()
    #     sns.heatmap(df)
    #     sns.plt.show()

    @staticmethod
    def ratings_demo_process(ratings_path, output_path):
        df = Results_Merge_Util.ratings_to_df_spark(ratings_path)
        sns.set()
        sns.heatmap(df)
        sns.plt.savefig(output_path)




        #     print(line.replace("[", ":{"), end='')
        # for line in fileinput.input(file_path, inplace=True):
        #     print(line.replace("]", "},"), end='')
        # for line in fileinput.input(file_path, inplace=True):
        #     print(line.replace("\t", ":"), end='')

        # with open(file_path) as recs_file:
        #     line = recs_file.readline()
        #     first_line_list = line.split()
        # print(first_line_list)




