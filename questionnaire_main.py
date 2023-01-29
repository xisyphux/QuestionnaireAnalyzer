import os
import pandas as pd

from data_pre_processor import pre_process_data
from cluster_algorithm.k_means_cluster import process_k_means_cluster_algorithm
from cluster_algorithm.k_modes_cluster import process_k_modes_cluster_algorithm
from result_picture.radviz_picture import radviz_plot, cluster_result_plot
from cluster_statistics import ClusterStatistics

pd.options.mode.chained_assignment = None
pd.options.display.unicode.east_asian_width = True

dirname = os.path.dirname(__file__)
output_dir = os.path.join(dirname, 'output')
if not os.path.exists(output_dir):
    os.mkdir(output_dir)

### Pre-process Questionnaire Data #########
_original_questionnaire_ = pd.read_csv(os.path.join(dirname, 'input/questionnaire_data.csv'), encoding='gb18030')
useful_column, cluster_column = pre_process_data(_original_questionnaire_, output_dir)

### Clustering Questionnaire Data ############
print('{:*^80}'.format(' Clustering Algorithm Starting '))
cluster_num = 16
useful_column, cluster_column = process_k_modes_cluster_algorithm(useful_column, cluster_column, cluster_num, output_dir)

### Draw Cluster Result Radviz Picture ############
print('{:*^80}'.format(' 用户画像聚类 '))
radviz_plot(cluster_column, output_dir)
# cluster_result_plot(cluster_column, cluster_num, output_dir)

### Statistic Each Cluster Score #########
print('\n{:*^80}'.format(' Clustering Statistics Starting '))
statistic = ClusterStatistics(useful_column, cluster_num, output_dir)
statistic.get_cluster_statistics()