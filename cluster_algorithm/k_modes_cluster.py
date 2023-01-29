import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_score, silhouette_samples
from sklearn import preprocessing
from kmodes.kmodes import KModes

def evaluate_k_modes_cluster(cluster_column: pd.DataFrame, random_seed: int, output_dir: str):
    cluster_num = range(2, 30)
    # subplot_counter = 1
    sc_scores = []
    costs = []
    for t in cluster_num:
        kmodes_model = KModes(n_clusters=t, init='Cao', random_state=random_seed, n_jobs=4).fit(cluster_column)

        sc_score = silhouette_score(cluster_column, kmodes_model.labels_, metric='euclidean')
        sc_scores.append(sc_score)
        costs.append(kmodes_model.cost_)

    plt.figure()
    plt.plot(cluster_num, sc_scores, '*-')
    plt.xlabel('Number of Clusters')
    plt.ylabel('Silhouette coefficient Score')
    plt.show()
    plt.savefig(os.path.join(output_dir, 'k_modes_sc.jpg'))

    plt.figure()
    # sns.lineplot(range(1, 16), costs, markers = 'o', color = 'red')
    plt.plot(cluster_num, costs, '*-')
    plt.title("Elbow")
    plt.xlabel('Number of clusters')
    plt.ylabel('Costs')
    plt.show()
    plt.savefig(os.path.join(output_dir, 'k_modes_elbow.jpg'))

def process_k_modes_cluster_algorithm(
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
    random_seed = 0
    evaluate_k_modes_cluster(cluster_column, random_seed, output_dir)

    kmodes_model = KModes(n_clusters=cluster_num, init='Cao', random_state=random_seed, n_jobs=4).fit(cluster_column)
    y_pred = kmodes_model.labels_ 
    whole_column['label'] = y_pred
    cluster_column['label'] = y_pred
    print("K-modes cost=", kmodes_model.cost_)
    print("K-modes Centers=", kmodes_model.cluster_centroids_)
    print("K-modes epoch_costs_=", kmodes_model.epoch_costs_)
    print("K-modes n_iter_=", kmodes_model.n_iter_)

    ### Save useful data to excel devided by label ###
    group = [whole_column.drop(index=whole_column.index) for i in range(cluster_num)]
    for index, series in whole_column.iterrows():
        group_id = series['label']
        group[group_id] = pd.concat([group[group_id], whole_column.loc[index].to_frame().T],axis=0)
    with pd.ExcelWriter(os.path.join(output_dir,"kmodes_result.xlsx")) as excel_writer:
        whole_column.to_excel(excel_writer, sheet_name="whole_data")
        for i in range(0, cluster_num):
            group_name = "group_" + str(i)
            group[i].to_excel(excel_writer, sheet_name=group_name)
    
    return whole_column, cluster_column