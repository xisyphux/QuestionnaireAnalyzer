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
if not os.path.exists(output_dir):
    os.mkdir(output_dir)

_original_questionnaire_ = pd.read_csv(os.path.join(dirname, 'input/questionnaire_data.csv'), encoding='gb18030')
cluster_column, useful_column = pre_processs_data(_original_questionnaire_, output_dir)

print("************************************************************************")
evaluate_k_means_cluster(cluster_column, output_dir)

cluster_num = 5

### K-means Cluster ###############################
# model = Pipeline([
#     # ('BN', preprocessing.StandardScaler()),('KMS', KMeans(n_clusters=cluster_num, n_init="auto", random_state=0))
#     ('BN', preprocessing.StandardScaler()),('KMS', KMeans(init="k-means++", n_clusters=cluster_num, n_init=50, random_state=420))
# ])
# kmeans_model = model.fit(cluster_column)
# y_pred = model.predict(cluster_column)
# useful_column['label'] = y_pred
# cluster_column['label'] = y_pred
# print(useful_column)

standard_column = preprocessing.MinMaxScaler().fit_transform(cluster_column)
kmeans_model = KMeans(n_clusters=cluster_num, init='k-means++', n_init="auto", random_state=420).fit(standard_column)
y_pred = kmeans_model.labels_
useful_column['label'] = y_pred
cluster_column['label'] = y_pred
print("K-means inertia=", kmeans_model.inertia_)
print("K-means Centers=", kmeans_model.cluster_centers_)

###################################################

### Draw Cluster Result Radviz Picture ############
plt.figure('用户画像聚类',figsize=(30, 15), dpi=320)
plt.title('radviz')
radviz(cluster_column.loc[:,:], class_column='label')
plt.show()
plt.savefig(os.path.join(output_dir,'user_portrait.jpg'))
###################################################

### Save useful data to excel devided by label ###
group = [useful_column.drop(index=useful_column.index) for i in range(cluster_num)]
for index, series in useful_column.iterrows():
    group_id = series['label']
    group[group_id] = pd.concat([group[group_id], useful_column.loc[index].to_frame().T],axis=0)
with pd.ExcelWriter(os.path.join(output_dir,"output.xlsx")) as excel_writer:
    useful_column.to_excel(excel_writer, sheet_name="whole_data")
    for i in range(0, cluster_num):
        group_name = "group_" + str(i)
        group[i].to_excel(excel_writer, sheet_name=group_name)
###################################################

print("************************************************************************")

statistic = ClusterStatistics(useful_column, cluster_num)
statistic.get_cluster_statistics()

# ERROR: Still can't figure out how this method works
# from pandas.plotting import andrews_curves
# plt.figure("useful_data_andrews_curves")
# plt.title('andrews_curves')
# andrews_curves(useful_column, 'label')
# plt.show()