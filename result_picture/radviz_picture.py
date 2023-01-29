import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import radviz
from sklearn.preprocessing import MinMaxScaler

def radviz_plot(cluster_column: pd.DataFrame, output_dir: str):
    ### Draw Cluster Result Radviz Picture ############
    plt.figure('用户画像聚类',figsize=(30, 15), dpi=320)
    plt.title('radviz')
    radviz(cluster_column.loc[:,:], class_column='label')
    plt.show()
    plt.savefig(os.path.join(output_dir,'user_radviz_portrait.jpg'))
    ###################################################

def cluster_result_plot(cluster_column: pd.DataFrame, cluster_num:int, output_dir:str):
    cluster_classification = [cluster_column.drop(index=cluster_column.index) for _ in range(cluster_num)]
    for index, series in cluster_column.iterrows():
        cluster_id = (int) (series['label'])
        cluster_classification[cluster_id] = pd.concat([cluster_classification[cluster_id], cluster_column.loc[index].to_frame().T], axis=0)

    features = []
    for i in range(cluster_num):
        cluster_classification[i] = cluster_classification[i].iloc[:,[0,1,2,3,4,5]]
        features.append(cluster_classification[i].describe().iloc[2,:])
        # print('\cluster_classification[', i, '] =\n', cluster_classification[i], ". \n", cluster_classification[i].describe(), ", \n", cluster_classification[i].describe().iloc[2,:])

    nums_min_max = MinMaxScaler().fit_transform(cluster_classification)
    print(nums_min_max.round(16))

    fig = plt.figure()
    ax = fig.add_subplot(111, polar=True)
    angles = np.linspace(0, 2 * np.pi, 6, endpoint=False)
    angles = np.concatenate((angles, [angles[0]]))
    colors = ['b', 'y', 'r', 'g', 'p', 'd']
    labels = (cluster_column['label'])
    labels = np.concatenate((labels, [labels[0]]))

    for i in range(cluster_num):
        temp_list = nums_min_max[i]
        temp = np.concatenate((temp_list, [temp_list[0]]))
        ax.plot(angles, temp, 'o-', colors=colors[i], label=i)

    ax.set_thetagrids(angles*180/np.pi, labels)
    ax.set_rlim(-0.2, 10)
    plt.title("用户画像聚类")
    plt.legend()
    plt.show()
    plt.savefig(os.path.join(output_dir,'user_portrait.jpg'))


# ERROR: Still can't figure out how this method works
# from pandas.plotting import andrews_curves
# plt.figure("useful_data_andrews_curves")
# plt.title('andrews_curves')
# andrews_curves(useful_column, 'label')
# plt.show()