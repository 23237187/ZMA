__author__ = 'WinterIsComing'

# Load Netflix dataset from files and merge them into a single table(file)

import numpy as np
import pandas as pd
from pandas import Series, DataFrame

def merge_files(file_path, data_table, file_num):

    df = pd.read_csv(file_path, header=None, skiprows=1)
    df = df.ix[:, :1]
    df = df.set_index(df.ix[:, 0])
    df = df.ix[:, 1]
    df.name = file_num
    data_table = pd.concat([data_table, df], axis=1)

    return data_table

def load_dataset(file_path, df):

    df = pd.read_csv(file_path)
    df = df.ix[:, 1:]
    df.index.name = 'usr'

    return df








