import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, silhouette_samples
import seaborn as sns
from sklearn import preprocessing

def evaluate_k_means_cluster(cluster_column: pd.DataFrame, random_state: int, output_dir: str):
    cluster_num = range(2, 30)
    cluster_column = preprocessing.MinMaxScaler().fit_transform(cluster_column)
    # subplot_counter = 1
    sc_scores = []
    for t in cluster_num:
        # subplot_counter += 1
        # plt.subplot(3, 2, subplot_counter)
        kmeans_model = KMeans(n_clusters=t, init='k-means++', n_init="auto", random_state=random_state).fit(cluster_column)

        # for i,l in enumerate(kmeans_model.labels_):
        #     plt.plot(x1[i], x2[i],color=colors[l], marker=markers[l], ls='None')
            # pic_name = 'table_k_' + str(t) + '_i_' + str(i) + '.jpg'
            # plt.savefig(pic_name)

        plt.xlim([0,15])
        plt.ylim([0,15])
        sc_score = silhouette_score(cluster_column, kmeans_model.labels_, metric='euclidean')
        sc_scores.append(sc_score)
        plt.title('K=%s, silhouette coefficient=%0.03f' %(t, sc_score))

    plt.figure()
    plt.plot(cluster_num, sc_scores, '*-')
    plt.xlabel('Number of Clusters')
    plt.ylabel('Silhouette coefficient Score')
    plt.show()
    plt.savefig(os.path.join(output_dir, 'k_means_sc.jpg'))

    wcss = []
    # print(cluster_num)
    for i in cluster_num:
        kmeans_model = KMeans(n_clusters=i, init='k-means++', n_init="auto", random_state=420).fit(cluster_column)
        wcss.append(kmeans_model.inertia_)

    plt.figure()
    # sns.lineplot(range(1, 16), wcss, markers = 'o', color = 'red')
    plt.plot(cluster_num, wcss, '*-')
    plt.title("Elbow")
    plt.xlabel('Number of clusters')
    plt.ylabel('WCSS')
    plt.show()
    plt.savefig(os.path.join(output_dir, 'k_means_elbow.jpg'))

def process_k_means_cluster_algorithm(
        whole_column: pd.DataFrame, 
        cluster_column: pd.DataFrame, 
        cluster_num: int, 
        output_dir: str) -> pd.DataFrame:
    """
    process_k_means_cluster_algorithm:
    Args:
        whole_column (pd.DataFrame): the whole column which contains all the questionnaire data.
        cluster_column (pd.DataFrame): the cluster column which is waiting for the clustering algorithm.
        cluster_num (int): the cluster number.
        output_dir (str): the output directory which the output excel or picture will be written to.
    Returns:
        Two pd.DataFrame: 
        (1) The whole related processed questionnaire data.
        (2) The cluster_column which will be used for k-means cluster.
    """

    random_state=420
    evaluate_k_means_cluster(cluster_column, random_state, output_dir)

    ### Pipeline K-means Cluster ###############################
    # model = Pipeline([
    #     # ('BN', preprocessing.StandardScaler()),('KMS', KMeans(n_clusters=cluster_num, n_init="auto", random_state=0))
    #     ('BN', preprocessing.StandardScaler()),('KMS', KMeans(init="k-means++", n_clusters=cluster_num, n_init=50, random_state=420))
    # ])
    # kmeans_model = model.fit(cluster_column)
    # y_pred = model.predict(cluster_column)
    # whole_column['label'] = y_pred
    # cluster_column['label'] = y_pred
    # print(whole_column)
    ##############################################################

    standard_column = preprocessing.MinMaxScaler().fit_transform(cluster_column)
    kmeans_model = KMeans(n_clusters=cluster_num, init='k-means++', n_init="auto", random_state=420).fit(standard_column)
    y_pred = kmeans_model.labels_
    whole_column['label'] = y_pred
    cluster_column['label'] = y_pred
    print("K-means inertia=", kmeans_model.inertia_)
    print("K-means Centers=", kmeans_model.cluster_centers_)

    ### Save useful data to excel devided by label ###
    group = [whole_column.drop(index=whole_column.index) for i in range(cluster_num)]
    for index, series in whole_column.iterrows():
        group_id = series['label']
        group[group_id] = pd.concat([group[group_id], whole_column.loc[index].to_frame().T],axis=0)
    with pd.ExcelWriter(os.path.join(output_dir,"output.xlsx")) as excel_writer:
        whole_column.to_excel(excel_writer, sheet_name="whole_data")
        for i in range(0, cluster_num):
            group_name = "group_" + str(i)
            group[i].to_excel(excel_writer, sheet_name=group_name)
    
    return whole_column, cluster_column