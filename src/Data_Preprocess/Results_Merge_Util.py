__author__ = 'root'

import pandas as pd
import ast
import glob
import fileinput


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



