import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


######################################################################################################################################
def create_values(raw_data, event_data):
    # We create different dataframe with the different tasks and we put inside it the part of the dataframe raw_data  that correspond
    #--------------------------------------------------------------------------------------------------------
    value1 = raw_data[raw_data['Time']==event_data.iloc[2,0]].index.item()
    value2 = raw_data[raw_data['Time']==event_data.iloc[3,0]].index.item()
    value3 = raw_data[raw_data['Time']==event_data.iloc[4,0]].index.item()
    value4 = raw_data[raw_data['Time']==event_data.iloc[5,0]].index.item()
    value5 = raw_data[raw_data['Time']==event_data.iloc[125,0]].index.item()
    value6 = raw_data[raw_data['Time']==event_data.iloc[126,0]].index.item()
    value7 = raw_data[raw_data['Time']==event_data.iloc[245,0]].index.item()
    value8 = raw_data[raw_data['Time']==event_data.iloc[246,0]].index.item()
    value9 = raw_data[raw_data['Time']==event_data.iloc[247,0]].index.item()
    #--------------------------------------------------------------------------------------------------------
    return value1,value2,value3,value4,value5,value6,value7,value8,value9
######################################################################################################################################


######################################################################################################################################
def create_tasks(raw_data, event_data):
    value1,value2,value3,value4,value5,value6,value7,value8,value9 = create_values(raw_data, event_data)
    start = raw_data.iloc[0:value1,:]
    open_eyes_1 = raw_data.iloc[value1:value2,:]
    close_eyes = raw_data.iloc[value2:value3,:]
    pause_1 = raw_data.iloc[value3:value4,:]
    IMG_TASK_1 = raw_data.iloc[value4:value5,:]
    pause_2 = raw_data.iloc[value5:value6,:]
    IMG_TASK_2 = raw_data.iloc[value6:value7,:]
    pause_3 = raw_data.iloc[value7:value8,:]
    open_eyes_2 = raw_data.iloc[value8:value9,:]
    
    return start, open_eyes_1, close_eyes, pause_1, IMG_TASK_1, pause_2, IMG_TASK_2, pause_3, open_eyes_2
######################################################################################################################################



######################################################################################################################################
def splite_10_seconds_by_10_seconds(raw_data, event_data):
    global start, pause_1
    start, open_eyes_1, close_eyes, pause_1, IMG_TASK_1, pause_2, IMG_TASK_2, pause_3, open_eyes_2 = create_tasks(raw_data, event_data)
    # Create several dataframe 10 seconds by 10 seconds for each taks. Here we need to do this for 7 variables
    #  -------------------------------------------- Start ----------------------------------------------
    start.set_index('Time', inplace=True) # put the column as index
    # --------------------------------------------------------------------------------------------------
    
    # -------------------------------------------- Open eyes_1 -----------------------------------------
    # Create group every 10 seconds
    open_eyes_1.set_index('Time', inplace=True) # put the column as index
    sliced_oe1 = open_eyes_1.groupby(open_eyes_1.index // 10) #there is 13 groups

    # Put these groups in different dataframe
    oe1_groups_dataframes = {}  # Dictionnaire pour stocker les DataFrames des groupes
    for group, group_df in sliced_oe1:
        name_of_variable = f"oe1_{int(group)}_df"
        oe1_groups_dataframes[group] = pd.DataFrame(group_df.copy())  # Stocker une copie du DataFrame du groupe
        globals()[name_of_variable] = oe1_groups_dataframes[group]
    # -------------------------------------------------------------------------------------------------

    # -------------------------------------------- Close eyes -----------------------------------------
    # Create group every 10 seconds
    close_eyes.set_index('Time', inplace=True) # put the column as index
    sliced_ce = close_eyes.groupby((close_eyes.index - close_eyes.index[0]) // 10)
    # Put these groups in different dataframe
    ce_groups_dataframes = {}  # Dictionnaire pour stocker les DataFrames des groupes
    for group, group_df in sliced_ce:
        name_of_variable = f"ce_{int(group)}_df"
        ce_groups_dataframes[group] = pd.DataFrame(group_df.copy())  # Stocker une copie du DataFrame du groupe
        globals()[name_of_variable] = ce_groups_dataframes[group]
    # ------------------------------------------------------------------------------------------------

    #  -------------------------------------------- pause_1 --------------------------------------------
    pause_1.set_index('Time', inplace=True) # put the column as index
    # --------------------------------------------------------------------------------------------------
    
    # -------------------------------------------- Img_Task_1 -----------------------------------------
    # Create group every 10 seconds
    IMG_TASK_1.set_index('Time', inplace=True) # put the column as index
    sliced_it1 = IMG_TASK_1.groupby((IMG_TASK_1.index - IMG_TASK_1.index[0]) // 10)
    # Put these groups in different dataframe
    it1_groups_dataframes = {}  # Dictionnaire pour stocker les DataFrames des groupes
    for group, group_df in sliced_it1:
        name_of_variable = f"it1_{int(group)}_df"
        it1_groups_dataframes[group] = pd.DataFrame(group_df.copy())  # Stocker une copie du DataFrame du groupe
        globals()[name_of_variable] = it1_groups_dataframes[group]
    # ------------------------------------------------------------------------------------------------

    # -------------------------------------------- pause_2 -----------------------------------------
    # Create group every 10 seconds
    pause_2.set_index('Time', inplace=True) # put the column as index
    sliced_p2 = pause_2.groupby((pause_2.index - pause_2.index[0]) // 10)
    # Put these groups in different dataframe
    p2_groups_dataframes = {}  # Dictionnaire pour stocker les DataFrames des groupes
    for group, group_df in sliced_p2:
        name_of_variable = f"p2_{int(group)}_df"
        p2_groups_dataframes[group] = pd.DataFrame(group_df.copy())  # Stocker une copie du DataFrame du groupe
        globals()[name_of_variable] = p2_groups_dataframes[group]
    # ------------------------------------------------------------------------------------------------

    # -------------------------------------------- Img_Task_2 -----------------------------------------
    # Create group every 10 seconds
    IMG_TASK_2.set_index('Time', inplace=True) # put the column as index
    sliced_it2 = IMG_TASK_2.groupby((IMG_TASK_2.index - IMG_TASK_2.index[0]) // 10)
    # Put these groups in different dataframe
    it2_groups_dataframes = {}  # Dictionnaire pour stocker les DataFrames des groupes
    for group, group_df in sliced_it2:
        name_of_variable = f"it2_{int(group)}_df"
        it2_groups_dataframes[group] = pd.DataFrame(group_df.copy())  # Stocker une copie du DataFrame du groupe
        globals()[name_of_variable] = it2_groups_dataframes[group]
    # ------------------------------------------------------------------------------------------------

    # -------------------------------------------- pause_3 -----------------------------------------
    # Create group every 10 seconds
    pause_3.set_index('Time', inplace=True) # put the column as index
    sliced_p3 = pause_3.groupby((pause_3.index - pause_3.index[0]) // 10)
    # Put these groups in different dataframe
    p3_groups_dataframes = {}  # Dictionnaire pour stocker les DataFrames des groupes
    for group, group_df in sliced_p3:
        name_of_variable = f"p3_{int(group)}_df"
        p3_groups_dataframes[group] = pd.DataFrame(group_df.copy())  # Stocker une copie du DataFrame du groupe
        globals()[name_of_variable] = p3_groups_dataframes[group]
    # ------------------------------------------------------------------------------------------------

    # -------------------------------------------- Open eyes_2 -----------------------------------------
    # Create group every 10 seconds
    open_eyes_2.set_index('Time', inplace=True) # put the column as index
    sliced_oe2 = open_eyes_2.groupby((open_eyes_2.index - open_eyes_2.index[0] )// 10) #there is 13 groups

    # Put these groups in different dataframe
    oe2_groups_dataframes = {}  # Dictionnaire pour stocker les DataFrames des groupes
    for group, group_df in sliced_oe2:
        name_of_variable = f"oe2_{int(group)}_df"
        oe2_groups_dataframes[group] = pd.DataFrame(group_df.copy())  # Stocker une copie du DataFrame du groupe
        globals()[name_of_variable] = oe2_groups_dataframes[group]
    # --------------------------------------------------------------------------------------------------
######################################################################################################################################
    