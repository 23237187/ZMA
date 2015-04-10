__author__ = 'WinterIsComing'

from sklearn.externals import joblib

from src import FCM

factors = joblib.load('nmf_model_100_factors.pkl')
print(factors)
print(factors.shape)
fuzzy_kmeans = FCM.FuzzyKMeans(k=3, m=2)
usr_clusters = fuzzy_kmeans.fit(factors)
print(usr_clusters.labels_)
print(usr_clusters.labels_.shape)

joblib.dump(usr_clusters, 'usr_clusters.pkl')
