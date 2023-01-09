import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, silhouette_samples

def evaluate_k_means_cluster(cluster_column: pd.DataFrame, output_dir: str):
    cluster_num = [4,5,6,7,8,9,10,11,12,13,14,15]
    subplot_counter = 1
    sc_scores = []
    for t in cluster_num:
        # subplot_counter += 1
        # plt.subplot(3, 2, subplot_counter)
        kmeans_model = KMeans(n_clusters=t, n_init="auto").fit(cluster_column)

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