#导入相关的库
import sys
import pandas as pd
import os
import random
import shutil
import numpy as np
import radiomics
from radiomics import featureextractor
import SimpleITK as sitk  

od.chdir("/data1/lzf/STAS/gdph/Code_radiomics")

para_path = "./config/feature.yaml"
extractor = featureextractor.RadiomicsFeatureExtractor(para_path) 
image_folder_path = "../original_image/processed_nii/"
seg_folder_path = "../original_image/segmentation/"

with open("./config/train_pos_id.txt", "r") as f:
    pos_id = eval(f.read())
with open("./config/train_neg_id.txt", "r") as f:
    neg_id = eval(f.read())
print(len(neg_id), len(pos_id))

id_all = {"pos": pos_id, "neg": neg_id}
for split in id_all:
    print("extract "+split+" feature.")
    features_dict = dict()
    df = pd.DataFrame()
    for index, path in enumerate(id_all[split]):
        image_path = os.path.join(image_folder_path, path+".nii.gz")
        seg_path = os.path.join(seg_folder_path, path+".nii.gz")
        features = extractor.execute(imageFilepath=image_path, maskFilepath=seg_path)
        features_dict['index'] = path
        for feature_key, feature_value in features.items():  #输出特征
            features_dict[feature_key] = feature_value
        df.append(pd.DataFrame.from_dict(features_dict.values()).T, ignore_index=True)
    df.columns = features_dict.keys()
    df.to_csv("./feature/"+split+"_feature.csv",index=0)
        