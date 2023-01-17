import os
import pandas as pd

class ClusterStatistics():
    def __init__(self, questionnaire_column: pd.DataFrame, cluster_num) -> None:
        self.cluster_num = cluster_num
        self.cluster_score = [questionnaire_column.drop(index=questionnaire_column.index) for _ in range(self.cluster_num)]
        for index, series in questionnaire_column.iterrows():
            cluster_id = series[28]
            self.cluster_score[cluster_id] = pd.concat([self.cluster_score[cluster_id], questionnaire_column.loc[index].to_frame().T], axis=0)

    def get_cluster_statistics(self):
        single_specie_score = pd.Series([0,0,0,0], index=["scenery", "farm", "participation", "ecology"])
        self.all_species_score = [single_specie_score.copy() for _ in range(self.cluster_num)]
        single_space_score = pd.Series([0,0,0,0,0,0,0,0,0,0,0,0,0,0], index=["Q12", "Q13", "Q14", "Q15", 
            "Q16", "Q17", "Q18", "Q19", "Q20", "Q21", "Q22","Q23", "Q24", "Q25"
        ])
        self.all_space_scores = [single_space_score.copy() for _ in range(self.cluster_num)]

        for i in range(self.cluster_num):
            print("cluster[", i, "] num:", len(self.cluster_score[i]))
            species_score = self.all_species_score[i]
            each_space_score = self.all_space_scores[i]

            ##########################################################################################
            ##########################################################################################

            # print("\t Q12 viewing_space score:", self.cluster_score[i]['viewing_space'].mean())
            # print("\t Q13 rest_space score:", self.cluster_score[i]['rest_space'].mean())
            # print("\t Q14 healthy_space score:", self.cluster_score[i]['healthy_space'].mean())
            # print("\t Q15 meeting_space score:", self.cluster_score[i]['meeting_space'].mean())
            each_space_score["Q12"] = self.cluster_score[i]['viewing_space'].mean()
            each_space_score["Q13"] = self.cluster_score[i]['rest_space'].mean()
            each_space_score["Q14"] = self.cluster_score[i]['healthy_space'].mean()
            each_space_score["Q15"] = self.cluster_score[i]['meeting_space'].mean()

            ##########################################################################################
            ##########################################################################################

            # print("\t Q16 picking_space score:", self.cluster_score[i]['picking_space'].mean())
            # print("\t Q17 dining_space score:", self.cluster_score[i]['dining_space'].mean())
            # print("\t Q18 sales_space score:", self.cluster_score[i]['sales_space'].mean())
            each_space_score["Q16"] = self.cluster_score[i]["picking_space"].mean()
            each_space_score["Q17"] = self.cluster_score[i]["dining_space"].mean()
            each_space_score["Q18"] = self.cluster_score[i]["sales_space"].mean()
            
            ##########################################################################################
            ##########################################################################################

            # print("\t Q19 recycling_space score:", self.cluster_score[i]['recycling_space'].mean())
            # print("\t Q20 sorting_space score:", self.cluster_score[i]['sorting_space'].mean())
            # print("\t Q21 reuse_space score:", self.cluster_score[i]['reuse_space'].mean())
            # print("\t Q22 anaimal_space score:", self.cluster_score[i]['anaimal_space'].mean())
            each_space_score["Q19"] = self.cluster_score[i]["recycling_space"].mean()
            each_space_score["Q20"] = self.cluster_score[i]["sorting_space"].mean()
            each_space_score["Q21"] = self.cluster_score[i]["reuse_space"].mean()
            each_space_score["Q22"] = self.cluster_score[i]["anaimal_space"].mean()

            ##########################################################################################
            ##########################################################################################

            # print("\t Q23 education_space score:", self.cluster_score[i]['education_space'].mean())
            # print("\t Q24 culture_space score:", self.cluster_score[i]['culture_space'].mean())
            # print("\t Q25 artistic_space score:", self.cluster_score[i]['artistic_space'].mean())
            each_space_score["Q23"] = self.cluster_score[i]["education_space"].mean()
            each_space_score["Q24"] = self.cluster_score[i]["culture_space"].mean()
            each_space_score["Q25"] = self.cluster_score[i]["artistic_space"].mean()

            ##########################################################################################
            ##########################################################################################

            species_score["scenery"] = (
                each_space_score["Q12"] + each_space_score["Q24"] + each_space_score["Q17"]
            )/3
            print("\t scenery score:", species_score["scenery"])

            species_score["farm"] = (
                each_space_score["Q16"] + each_space_score["Q25"] + each_space_score["Q23"]
            )/3
            print("\t farm_score:", species_score["farm"])

            species_score["participation"] = (
                each_space_score["Q13"] + each_space_score["Q14"] + each_space_score["Q15"]
            )/3
            print("\t participation_score:", species_score["participation"])

            species_score["ecology"] = (
                each_space_score["Q19"] + each_space_score["Q20"] + each_space_score["Q21"]
            )/3
            print("\t ecology_score:", species_score["ecology"])
        
        for i in range(self.cluster_num):
            species_score = self.all_species_score[i].sort_values(ascending=False, inplace=False)
            print("cluster[", i, "] species score:", species_score.index)
            # each_space_score = self.all_space_scores[i].sort_values(ascending=False, inplace=False)
            # print("cluster[", i, "] space score:", each_space_score.index)
            



    
    def get_scenery_space_statistics(self):
        pass

    def get_farm_space_statistics(self):
        pass

    def get_recycle_space_statistics(self):
        pass

    def get_learn_space_statistics(self):
        pass