__author__ = 'WinterIsComing'

from sklearn.decomposition import NMF
from sklearn.externals import joblib

from src.Netflix_Dataset_Preprocess import *


df = load_dataset('D:/Work/Dataset/Netflix/training_set/test_table.csv')
df = df.values()

factors = NMF.fit(df)
joblib.dump(factors, 'nmf_model.pkl')


