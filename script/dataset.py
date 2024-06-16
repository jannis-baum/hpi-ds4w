import json
import os

import pandas as pd

from definitions import features_path

data_dir = 'data'
dataset_path = os.path.join(data_dir, 'dataset.csv')
emg_cols = [f'EMG_{i}' for i in range(8)]
emg_cols_cal = [f'{col}_cal' for col in emg_cols]

# X (EMG data), y (labels)
DataSet = tuple[pd.DataFrame, pd.DataFrame]

def get_data(calibrated = True) -> DataSet:
    dataset = pd.read_csv(dataset_path)
    label_cols = [col for col in dataset.columns if col not in emg_cols + emg_cols_cal]
    X = dataset[emg_cols_cal if calibrated else emg_cols]
    y = dataset[label_cols]
    return (X, y)

def get_feature_list():
    with open(features_path, 'r') as fp:
        return json.load(fp)
