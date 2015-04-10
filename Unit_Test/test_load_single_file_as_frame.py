__author__ = 'WinterIsComing'

from src.Netflix_Dataset_Preprocess import *

file_path_prefix = 'D:/Work/Dataset/Netflix/training_set/'
data_table = DataFrame()

for i in range(1,1000):
    file_path_suffix = "mv_%07d" % i + '.txt'
    file_path = file_path_prefix + file_path_suffix
    data_table = merge_files(file_path, data_table, i)

data_table.to_csv(file_path_prefix + 'test_table.csv')


