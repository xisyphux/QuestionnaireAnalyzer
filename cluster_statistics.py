import os
import pandas as pd

class ClusterStatistics():
    def __init__(self, questionnaire_column: pd.DataFrame, cluster_num, output_dir: str) -> None:
        self.cluster_num = cluster_num
        self.output_dir = output_dir
        # self.classify_questionnaire(questionnaire_column)
        # questionnaire_column = self.reword_questionnaire(questionnaire_column)
        # questionnaire_column.to_excel(os.path.join(output_dir, "rework_selected_column.xlsx"))

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

            # print("\t Q12 viewing_space score:", self.cluster_score[i]['Q12'].mean())
            # print("\t Q13 rest_space score:", self.cluster_score[i]['Q13'].mean())
            # print("\t Q14 healthy_space score:", self.cluster_score[i]['Q14'].mean())
            # print("\t Q15 meeting_space score:", self.cluster_score[i]['Q15'].mean())
            each_space_score["Q12"] = self.cluster_score[i]['Q12'].mean()
            each_space_score["Q13"] = self.cluster_score[i]['Q13'].mean()
            each_space_score["Q14"] = self.cluster_score[i]['Q14'].mean()
            each_space_score["Q15"] = self.cluster_score[i]['Q15'].mean()

            ##########################################################################################
            ##########################################################################################

            # print("\t Q16 picking_space score:", self.cluster_score[i]['Q16'].mean())
            # print("\t Q17 dining_space score:", self.cluster_score[i]['Q17'].mean())
            # print("\t Q18 sales_space score:", self.cluster_score[i]['Q18'].mean())
            each_space_score["Q16"] = self.cluster_score[i]["Q16"].mean()
            each_space_score["Q17"] = self.cluster_score[i]["Q17"].mean()
            each_space_score["Q18"] = self.cluster_score[i]["Q18"].mean()
            
            ##########################################################################################
            ##########################################################################################

            # print("\t Q19 recycling_space score:", self.cluster_score[i]['Q19'].mean())
            # print("\t Q20 sorting_space score:", self.cluster_score[i]['Q20'].mean())
            # print("\t Q21 reuse_space score:", self.cluster_score[i]['Q21'].mean())
            # print("\t Q22 anaimal_space score:", self.cluster_score[i]['Q22'].mean())
            each_space_score["Q19"] = self.cluster_score[i]["Q19"].mean()
            each_space_score["Q20"] = self.cluster_score[i]["Q20"].mean()
            each_space_score["Q21"] = self.cluster_score[i]["Q21"].mean()
            each_space_score["Q22"] = self.cluster_score[i]["Q22"].mean()

            ##########################################################################################
            ##########################################################################################

            # print("\t Q23 education_space score:", self.cluster_score[i]['Q23'].mean())
            # print("\t Q24 culture_space score:", self.cluster_score[i]['Q24'].mean())
            # print("\t Q25 artistic_space score:", self.cluster_score[i]['Q25'].mean())
            each_space_score["Q23"] = self.cluster_score[i]["Q23"].mean()
            each_space_score["Q24"] = self.cluster_score[i]["Q24"].mean()
            each_space_score["Q25"] = self.cluster_score[i]["Q25"].mean()

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
            
    def classify_questionnaire(self, questionnaire_column: pd.DataFrame) -> None:
        self.majority_cloud =[questionnaire_column.drop(index=questionnaire_column.index) for _ in range(7)]
        for index, series in questionnaire_column.iterrows():
            scenery_score = (series["Q12"] + series["Q24"] + series["Q17"])/3
            farm_score = (series["Q16"] + series["Q25"] + series["Q23"])/3
            participation_score = (series["Q13"] + series["Q14"] + series["Q15"])/3
            ecology_score = (series["Q19"] + series["Q20"] + series["Q21"])/3
            if participation_score>ecology_score and ecology_score>scenery_score and scenery_score>farm_score:
                self.majority_cloud[0] = pd.concat([self.majority_cloud[0], questionnaire_column.loc[index].to_frame().T], axis=0)
            elif participation_score>ecology_score and ecology_score>farm_score and farm_score>scenery_score:
                self.majority_cloud[1] = pd.concat([self.majority_cloud[1], questionnaire_column.loc[index].to_frame().T], axis=0)
            elif participation_score>scenery_score and scenery_score>ecology_score and ecology_score>farm_score:
                self.majority_cloud[2] = pd.concat([self.majority_cloud[2], questionnaire_column.loc[index].to_frame().T], axis=0)
            elif participation_score>scenery_score and scenery_score>farm_score and farm_score> ecology_score:
                self.majority_cloud[3] = pd.concat([self.majority_cloud[3], questionnaire_column.loc[index].to_frame().T], axis=0)
            elif participation_score>farm_score and farm_score>ecology_score and ecology_score>scenery_score:
                self.majority_cloud[4] = pd.concat([self.majority_cloud[4], questionnaire_column.loc[index].to_frame().T], axis=0)
            elif participation_score>farm_score and farm_score>scenery_score and scenery_score>farm_score:
                self.majority_cloud[5] = pd.concat([self.majority_cloud[5], questionnaire_column.loc[index].to_frame().T], axis=0)
            else:
                self.majority_cloud[6] = pd.concat([self.majority_cloud[6], questionnaire_column.loc[index].to_frame().T], axis=0)
        
        with pd.ExcelWriter(os.path.join(self.output_dir, "majority_cloud.xlsx")) as excel_writer:
            for i in range(7):
                group_name = "majority_" + str(i)
                self.majority_cloud[i].to_excel(excel_writer, sheet_name=group_name)

    def reword_questionnaire(self, questionnaire_column: pd.DataFrame) -> pd.DataFrame:
        for index, series in questionnaire_column.iterrows():
            series = series.copy()
            species = ["viewing_space", "rest_space", "healthy_space", "meeting_space", "picking_space", "dining_space", "sales_space", "recycling_space", "sorting_space", "reuse_space", "anaimal_space", "education_space", "culture_space", "artistic_space"]
            for i in species:
                if series[i] > 7:
                    questionnaire_column.loc[index, i] = 3
                elif series[i] > 4:
                    questionnaire_column.loc[index, i] = 2
                else:
                    questionnaire_column.loc[index, i] = 1
        return questionnaire_column



    
    def get_scenery_space_statistics(self):
        pass

    def get_farm_space_statistics(self):
        pass

    def get_recycle_space_statistics(self):
        pass

    def get_learn_space_statistics(self):
        pass