__author__ = 'WinterIsComing'

import sys

import os
import itertools
import re

import ast
import csv

import numpy as np
import pandas as pd
from pandas import Series, DataFrame

import sklearn.metrics.pairwise as pw

def cluster_raw_file_2_cluster_csv(cluster_path, output_path):

    clusters_dict = dict()
    points_frame = DataFrame()
    for i in range(3):
        with open(cluster_path + ('/cluster_%d' % i)) as cluster_file:
            first_line = cluster_file.readline()
            list_raw_cluster_info = first_line.strip().split(':')
            # print(*list_raw_cluster_info, sep='\n')
            cluster_centroid_coordinates = list_raw_cluster_info[2].strip().split("\"")[0].strip(',')
            cluster_centroid_coordinates = ast.literal_eval(cluster_centroid_coordinates)
            cluster_points_num = list_raw_cluster_info[3].strip().split(",")[0]
            cluster_identifier = list_raw_cluster_info[4].strip('}').strip("\"")
            # print("====================================================================")
            # print(cluster_centroid_coordinates)
            # print(cluster_points_num)
            # print(cluster_identifier)
            clusters_dict.update({cluster_identifier: cluster_centroid_coordinates})
            cluster_file.readline()
            # cluster_file.readline()
            # list_tmp = cluster_file.readline().strip().split(':')
            # print(*list_tmp, sep='\n')
            # print("====================================================================")
            points_cor_lists = list()
            for line in cluster_file:
                if line.strip():
                    point_coordinates = ast.literal_eval(line.split(':')[2].strip())
                    points_cor_lists.append(point_coordinates)
            # print(points_cor_lists)
            with open(output_path + "/points.csv", "a", newline='') as points_csv:
                csv_writer = csv.writer(points_csv)
                csv_writer.writerows(points_cor_lists)

    # print(clusters_dict)
    df = DataFrame.from_dict(clusters_dict, orient='index')
    df.to_csv(output_path + '/clusters.csv', header=None)
    # print(df)
    # df = pd.read_csv('points.csv', header=None)
    # print(df)

def split_cluster_file(raw_cluster_file_path, pattern_string=r'{.*}'):
    print(raw_cluster_file_path)
    r = re.compile(pattern_string)
    with open(raw_cluster_file_path + '/cluster555') as raw_cluster_file:
        i = 0
        for k,g in itertools.groupby(raw_cluster_file, key=lambda x:r.search(x)):
            with open (raw_cluster_file_path + ('/cluster_%d' % i), 'a') as cluster_file_head:
                if k:
                    print(k.group(0), file=cluster_file_head)
                else:
                    for item in list(g):
                        print(item, file=cluster_file_head)
                    i = i + 1
        print(i)

def generate_probability_vector_result(output_path):

    cluster_frame = pd.read_csv(output_path + '/clusters.csv', header=None)
    cluster_frame = cluster_frame.set_index(cluster_frame.ix[:,0]).ix[:, 1:]
    cluster_array = cluster_frame.values

    points_frame = pd.read_csv(output_path + '/points.csv', header=None)
    # points_frame = points_frame.drop_duplicates()
    points_array = points_frame.values

    distance_matrix = pw.euclidean_distances(cluster_array, points_array)
    distance_matrix = distance_matrix.T
    distance_frame = DataFrame(distance_matrix)
    # print(distance_frame)
    # print(distance_frame.sum(axis=1))
    distance_frame = distance_frame.div(distance_frame.sum(axis=1), axis=0)
    distance_frame.to_csv(output_path + '/probability.csv')

def split_parse_generate(input_path, output_path):

    split_cluster_file(input_path)
    cluster_raw_file_2_cluster_csv(input_path, output_path)
    generate_probability_vector_result(output_path)




# if __name__ == "__main__":
#     print(sys.argv)
#     input_path = sys.argv[1]
#     output_path = sys.argv[2]
#     split_cluster_file(input_path, output_path)