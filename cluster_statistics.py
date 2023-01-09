import os
import pandas as pd

class ClusterStatistics():
    def __init__(self, questionnaire_column: pd.DataFrame, cluster_num) -> None:
        self.cluster_num = cluster_num
        self.cluster = [questionnaire_column.drop(index=questionnaire_column.index) for i in range(self.cluster_num)]
        for index, series in questionnaire_column.iterrows():
            cluster_id = series[28]
            self.cluster[cluster_id] = pd.concat([self.cluster[cluster_id], questionnaire_column.loc[index].to_frame().T], axis=0)

    def get_cluster_statistics(self):
        for i in range(self.cluster_num):
            print("cluster[", i, "] num:", len(self.cluster[i]))
            print("\t Q12 viewing_space score:", self.cluster[i]['viewing_space'].mean())
            print("\t Q13 rest_space score:", self.cluster[i]['rest_space'].mean())
            print("\t Q14 healthy_space score:", self.cluster[i]['healthy_space'].mean())
            print("\t Q15 meeting_space score:", self.cluster[i]['meeting_space'].mean())
            print("\t Q16 picking_space score:", self.cluster[i]['picking_space'].mean())
            print("\t Q17 dining_space score:", self.cluster[i]['dining_space'].mean())
            print("\t Q18 sales_space score:", self.cluster[i]['sales_space'].mean())
            print("\t Q19 recycling_space score:", self.cluster[i]['recycling_space'].mean())
            print("\t Q20 sorting_space score:", self.cluster[i]['sorting_space'].mean())
            print("\t Q21 reuse_space score:", self.cluster[i]['reuse_space'].mean())
            print("\t Q22 anaimal_space score:", self.cluster[i]['anaimal_space'].mean())
            print("\t Q23 education_space score:", self.cluster[i]['education_space'].mean())
            print("\t Q24 culture_space score:", self.cluster[i]['culture_space'].mean())
            print("\t Q25 artistic_space score:", self.cluster[i]['artistic_space'].mean())
