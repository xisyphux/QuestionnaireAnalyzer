import os
import pandas as pd
from question_map import *

def pre_processs_data(questionnaire_data: pd.DataFrame, output_dir: str) -> pd.DataFrame:
    """
    Pre-process the questionnaire data to make it ready to be used in the training process.
    including: 
        (1) extract useful data from the original questionnaire data.
        (2) remove duplcated values.
        (3) remove illegal values.

    Args:
        questionnaire_data (pd.DataFrame): The questionnaire data.
        output_dir (str): The output directory.

    Returns:
        Two pd.DataFrame: 
        (1) The cluster_column which will be used for k-means cluster.
        (2) The whole related processed questionnaire data.
    """

    selected_column = questionnaire_data.iloc[:,[2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,32,33,34]]
    duplicated_data = selected_column.drop(index=selected_column.index)
    print("Original questionarire column index length is ", len(selected_column), '\n')
    print("Original column is:\n", selected_column, "\n")

    duplicated_data = selected_column[selected_column.duplicated(keep=False)]
    selected_column = selected_column.drop_duplicates(subset=None, inplace=False)
    print("There are ", len(duplicated_data), " duplicated columns in questionarire column.")
    print("After drop duplicate columns, Length of remaining questionarire column index is ", len(selected_column), '\n')
    duplicated_data.to_excel(os.path.join(output_dir, "duplicated_data.xlsx"))
    

    illegal_column = selected_column.drop(index=selected_column.index)
    for index, series in selected_column.iterrows():
        for j in range(11,24):
            if (series[j] != series[j+1]):
                break
            if (j == 23):
                illegal_column = pd.concat([illegal_column, selected_column.loc[index].to_frame().T], axis=0)
                selected_column = selected_column.drop(index, axis=0)
    print("There are ", len(illegal_column), " illegal columns in questionarire column.")
    print("After drop illegal columns, Length of useful questionarire column index is ", len(selected_column), '\n')
    illegal_column.to_excel(os.path.join(output_dir, "illegal_column.xlsx"))

    selected_column.columns = selected_column.columns.str.replace('Q1_您的性别', 'sex')
    selected_column.columns = selected_column.columns.str.replace('Q2_您的年龄', 'age')
    selected_column.columns = selected_column.columns.str.replace('Q3_您的最高学历（含目前在读）是？', 'education')
    selected_column.columns = selected_column.columns.str.replace('Q4_您目前的职业是？', 'profession')
    selected_column.columns = selected_column.columns.str.replace('Q5_您的平均税前年收入是多少元？（包括薪资、理财、固定资产收租等）', 'annual_pay')
    selected_column.columns = selected_column.columns.str.replace('Q6_您家中常住成员是？', 'family_num')
    selected_column.columns = selected_column.columns.str.replace('Q7_您目前居住的房屋是？', 'residence_type')
    selected_column.columns = selected_column.columns.str.replace('Q8_您所居住的社区活动空间以及绿化环境如何？', 'community_space')
    selected_column.columns = selected_column.columns.str.replace('Q9_您在社区的户外活动（散步、娱乐休憩等）频率大约是多久？', 'exercise_frequency')
    selected_column.columns = selected_column.columns.str.replace('Q10_以下的屋顶花园形式您更偏爱哪种？', 'form_preference')
    selected_column.columns = selected_column.columns.str.replace('Q11_如果您所在的社区建成屋顶花园是否想去活动？', 'participation_willingness')
    selected_column.columns = selected_column.columns.str.replace('Q12_花卉、草坪、树木等植物观赏空间', 'viewing_space')
    selected_column.columns = selected_column.columns.str.replace('Q13_喝茶、阅读、冥想、休闲等休憩空间', 'rest_space')
    selected_column.columns = selected_column.columns.str.replace('Q14_散步、慢跑、瑜伽、乒乓球、羽毛球等运动健康空间', 'healthy_space')
    selected_column.columns = selected_column.columns.str.replace('Q15_聊天、派对、沙龙等聚会空间', 'meeting_space')
    selected_column.columns = selected_column.columns.str.replace('Q16_新鲜无污染的瓜果蔬菜等农作物种植采摘空间', 'picking_space')
    selected_column.columns = selected_column.columns.str.replace('Q17_冷餐会、果蔬轻食分享等餐饮空间', 'dining_space')
    selected_column.columns = selected_column.columns.str.replace('Q18_果蔬集市、跳蚤市场等展示销售空间', 'sales_space')
    selected_column.columns = selected_column.columns.str.replace('Q19_雨水收集、污水处理等水资源回收利用空间', 'recycling_space')
    selected_column.columns = selected_column.columns.str.replace('Q20_厨余垃圾堆肥、废旧物再利用等垃圾精细化分类空间', 'sorting_space')
    selected_column.columns = selected_column.columns.str.replace('Q21_光伏发电、太阳能照明等再生能源利用空间', 'reuse_space')
    selected_column.columns = selected_column.columns.str.replace('Q22_城市蜂房、生态鸟屋等动物友好空间', 'anaimal_space')
    selected_column.columns = selected_column.columns.str.replace('Q23_识农教育、植物认知、昆虫观察等儿童自然教育空间', 'education_space')
    selected_column.columns = selected_column.columns.str.replace('Q24_体现社区文化的艺术装置、景观雕塑等', 'culture_space')
    selected_column.columns = selected_column.columns.str.replace('Q25_画展、音乐会、节庆活动等艺文空间', 'artistic_space')

    # cluster_column = selected_column.iloc[:, [0,1,2,3,4,5,6,7,8]]
 
    # cluster_column['sex'] = cluster_column.loc[:,'sex'].map(sex_map)
    # cluster_column['age'] = cluster_column['age'].map(age_map)
    # cluster_column['education'] = cluster_column['education'].map(education_map)
    # cluster_column['profession'] = cluster_column['profession'].map(profession_map)
    # cluster_column['annual_pay'] = cluster_column['annual_pay'].map(annual_pay_map)
    # cluster_column['family_num'] = cluster_column['family_num'].map(family_num_map)
    # cluster_column['residence_type'] = cluster_column['residence_type'].map(residence_type_map)
    # cluster_column['community_space'] = cluster_column['community_space'].map(community_space_map)
    # cluster_column['exercise_frequency'] = cluster_column['exercise_frequency'].map(exercise_frequency_map)
    # print('In cluster_column, nan_num=',cluster_column.isnull().sum().sum(), ", replace them.")
    # cluster_column = cluster_column.fillna(value={'profession':12, 'family_num':4})
    # print("Digital Column is: \n", cluster_column, "\n")

    cluster_column = selected_column.iloc[:, [1,2,4,5,8]]
    print(cluster_column)

    # cluster_column['sex'] = cluster_column.loc[:,'sex'].map(sex_map)
    cluster_column['age'] = cluster_column['age'].map(age_map)
    cluster_column['education'] = cluster_column['education'].map(education_map)
    # cluster_column['profession'] = cluster_column['profession'].map(profession_map)
    cluster_column['annual_pay'] = cluster_column['annual_pay'].map(annual_pay_map)
    cluster_column['family_num'] = cluster_column['family_num'].map(family_num_map)
    # cluster_column['residence_type'] = cluster_column['residence_type'].map(residence_type_map)
    # cluster_column['community_space'] = cluster_column['community_space'].map(community_space_map)
    cluster_column['exercise_frequency'] = cluster_column['exercise_frequency'].map(exercise_frequency_map)
    print('In cluster_column, nan_num=',cluster_column.isnull().sum().sum(), ", replace them.")
    cluster_column = cluster_column.fillna(value={'profession':12, 'family_num':4})
    print("Digital Column is: \n", cluster_column, "\n")

    print("------------------------------------------------------------------------\n")
    cluster_column.to_excel(os.path.join(output_dir, "cluster_column.xlsx"))
    selected_column.to_excel(os.path.join(output_dir, "selected_column.xlsx"))

    return cluster_column, selected_column