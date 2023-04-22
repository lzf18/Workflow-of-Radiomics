from scipy.stats import levene, ttest_ind
import pandas as pd

def SelectFeatureByPvalue(feature_df, test="t-test", p_value=0.05, info_columns=["index", "label"]):
    """
    Select features by test
    :param feature_df: the feature dataframe including index, label, feature1, feature2...
    :param test: the method of test
    :param p_value: the threshold of p value
    :param info_columns: column names that are not feature names
    :return columns_index: a list of feature names that are selected
    """
    
    feature_df = feature_df.copy(deep=True)
    # creat new df of different label
    classinformation = feature_df["label"].unique()
    for temp_classinformation in classinformation:
        temp_data = feature_df[feature_df['label'].isin([temp_classinformation])]
        exec("df%s=temp_data"%temp_classinformation)
        
    counts = 0
    columns_index =[]
    for column_name in feature_df.columns:
        if column_name in info_columns:
            continue
        # TODO: add more test methods
        if levene(df1[column_name], df0[column_name])[1] > 0.05:
            if ttest_ind(df1[column_name],df0[column_name],equal_var=True)[1] < 0.05:
                columns_index.append(column_name)
        else:
            if ttest_ind(df1[column_name],df0[column_name],equal_var=False)[1] < 0.05:
                columns_index.append(column_name)
    columns_index = info_columns + columns_index
    
    return columns_index

def NormalizeFeature(feature_df, info_columns=["index", "label"]):
    """
    Normalize features and return mean and std of each feature
    :param feature_df: the feature dataframe including index, label, feature1, feature2...
    :param info_columns: column names that are not feature names
    :return feature_nor_df: the feature dataframe after normalizing
    :return mean_dict: a dict to store mean of each feature
    :return std_dict: a dict to store std of each feature
    """
    
    feature_df = feature_df.copy(deep=True)
    
    # calculate mean and std
    mean_dict = {}
    std_dict = {}
    for column_name in feature_df.columns:
        if column_name in infor_columns:
            continue
        else:
            data = np.asarray(feature_df[column_name].to_list())
            mean_dict[column_name] = np.mean(data)
            std_dict[column_name] = np.std(data)
    # normalize
    for column_name in feature_df.columns:
        if column_name in info_columns:
            continue
        else:
            feature_df[column_name] = feature_df[column_name].apply(lambda x: (x-mean_dict[column_name])/std_dict[column_name])
    return feature_df, mean_dict, std_dict



    
    
    