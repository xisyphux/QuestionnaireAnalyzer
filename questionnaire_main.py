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
import seaborn as sns

pd.options.mode.chained_assignment = None
pd.options.display.unicode.east_asian_width = True

dirname = os.path.dirname(__file__)
output_dir = os.path.join(dirname, 'output')

_original_questionnaire_ = pd.read_csv(os.path.join(dirname, 'input/questionnaire_data.csv'), encoding='gb18030')
cluster_column, useful_column = pre_processs_data(_original_questionnaire_, output_dir)

# plt.figure(figsize=(20,20), dpi=200)
# plt.subplot(3,3,1)
# sns.boxplot(x = 'sex', data = cluster_column)
#
# plt.subplot(3,3,2)
# sns.boxplot(x = 'age', data = cluster_column)
#
# plt.subplot(3,3,3)
# sns.boxplot(x = 'education', data = cluster_column)
#
# plt.subplot(3,3,4)
# sns.boxplot(x = 'profession', data = cluster_column)
#
# plt.subplot(3,3,5)
# sns.boxplot(x = 'annual_pay', data = cluster_column)
#
# plt.subplot(3,3,6)
# sns.boxplot(x = 'family_num', data = cluster_column)
#
# plt.subplot(3,3,7)
# sns.boxplot(x = 'residence_type', data = cluster_column)
#
# plt.subplot(3,3,8)
# sns.boxplot(x = 'community_space', data = cluster_column)
#
# plt.subplot(3,3,9)
# sns.boxplot(x = 'exercise_frequency', data = cluster_column)
# plt.show()

# corrmat = cluster_column.corr()
# print(corrmat)
# f, ax = plt.subplots(figsize=(12, 9))
# sns.heatmap(corrmat, vmax=.08, square=True)

print("************************************************************************")
evaluate_k_means_cluster(cluster_column, output_dir)


cluster_num = 5

model = Pipeline([
    # ('BN', preprocessing.StandardScaler()),('KMS', KMeans(n_clusters=cluster_num, n_init="auto", random_state=0))
    ('BN', preprocessing.StandardScaler()),('KMS', KMeans(init="k-means++", n_clusters=cluster_num, n_init=50, random_state=420))
 ])
model.fit(cluster_column)
# joblib.dump(model, "./model/model.pkl")
# model = joblib.load("./model/model.pkl")
y_pred = model.predict(cluster_column)

print('result')
print(y_pred)

plt.scatter(cluster_column['education'], cluster_column['annual_pay'], c = y_pred)
plt.xlabel('education')
plt.ylabel('annual_pay')
plt.show()

# useful_column['label'] = y_pred
# cluster_column['label'] = y_pred

# plt.figure('用户画像聚类',figsize=(30, 15), dpi=320)
# plt.title('radviz')
# radviz(cluster_column.loc[:,:], class_column='label')
# plt.show()
# plt.savefig(os.path.join(output_dir,'user_portrait.jpg'))

#* print(useful_column)
# useful_column.to_excel("./useful_column.xlsx", encoding='gb18030')

#* statistic = ClusterStatistics(useful_column, cluster_num)
#* statistic.get_cluster_statistics()







# ERROR: Still can't figure out how this method works
# from pandas.plotting import andrews_curves
# plt.figure("useful_data_andrews_curves")
# plt.title('andrews_curves')
# andrews_curves(useful_column, 'label')
# plt.show()