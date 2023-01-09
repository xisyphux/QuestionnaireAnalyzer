import os
import pandas as pd
from pandas.plotting import radviz
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.pipeline import Pipeline
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, silhouette_samples
from data_pre_processsor import pre_processs_data
from k_means_cluster_evaluate import evaluate_k_means_cluster
from cluster_statistics import ClusterStatistics

pd.options.mode.chained_assignment = None
pd.options.display.unicode.east_asian_width = True

dirname = os.path.dirname(__file__)
output_dir = os.path.join(dirname, 'output')

_original_questionnaire_ = pd.read_csv(os.path.join(dirname, 'input/questionnaire_data.csv'), encoding='gb18030')
cluster_column, useful_column = pre_processs_data(_original_questionnaire_, output_dir)

print("************************************************************************")
evaluate_k_means_cluster(cluster_column, output_dir)


cluster_num = 6

model = Pipeline([
    # ('BN', preprocessing.StandardScaler()),('KMS', KMeans(n_clusters=cluster_num, n_init="auto", random_state=0))
    ('BN', preprocessing.StandardScaler()),('KMS', KMeans(init="k-means++", n_clusters=cluster_num, n_init=50, random_state=420))
])
model.fit(cluster_column)
# joblib.dump(model, "./model/model.pkl")
# model = joblib.load("./model/model.pkl")
y_pred = model.predict(cluster_column)

useful_column['label'] = y_pred
cluster_column['label'] = y_pred

# plt.figure('用户画像聚类',figsize=(30, 15), dpi=320)
# plt.title('radviz')
# radviz(cluster_column.loc[:,:], class_column='label')
# plt.show()
# plt.savefig(os.path.join(output_dir,'user_portrait.jpg'))

print(useful_column)
# useful_column.to_excel("./useful_column.xlsx", encoding='gb18030')

statistic = ClusterStatistics(useful_column, cluster_num)
statistic.get_cluster_statistics()

# ERROR: Still can't figure out how this method works
# from pandas.plotting import andrews_curves
# plt.figure("useful_data_andrews_curves")
# plt.title('andrews_curves')
# andrews_curves(useful_column, 'label')
# plt.show()