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

os.chdir("/data1/lzf/STAS/code_rd")

para_path = "./config/feature.yaml"
extractor = featureextractor.RadiomicsFeatureExtractor(para_path) 
image_folder_path = "../processed_nii/image/"
seg_folder_path = "../processed_nii/seg/"
split = "test"

# get patients' id
with open("./config/"+split+"_pos_id.txt", "r") as f:
    pos_id = eval(f.read())
with open("./config/"+split+"_neg_id.txt", "r") as f:
    neg_id = eval(f.read())
print(len(neg_id), len(pos_id))

id_all = {"pos": pos_id, "neg": neg_id}

for pos_or_neg in id_all:
    print("extract "+pos_or_neg+" feature.")
    features_dict = dict()
    df = pd.DataFrame()
    for index, path in enumerate(id_all[pos_or_neg]):
        try:
            # extract features and store in df
            image_path = os.path.join(image_folder_path, path+".nii.gz")
            seg_path = os.path.join(seg_folder_path, path+".nii.gz")
            features = extractor.execute(imageFilepath=image_path, maskFilepath=seg_path)
            features_dict['index'] = path
            for feature_key, feature_value in features.items():
                features_dict[feature_key] = feature_value
            df = pd.concat([df, pd.DataFrame.from_dict(features_dict, orient='index').T], axis=0, ignore_index=True)
        except Exception as e:
            with open("./config/except.txt", "a") as f:
                f.write(str(e))
    df.columns = features_dict.keys()
    df.to_csv("./feature/"+split+"_"+pos_or_neg+"_feature.csv",index=0)
    
        