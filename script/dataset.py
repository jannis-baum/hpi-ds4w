import json
import os

import pandas as pd

from definitions import features_path

data_dir = 'data'
dataset_path = os.path.join(data_dir, 'dataset.csv')

col_hold = 'hold'
# id is '{day}_{person_id}_{recording}_{set_index}'
col_id = 'id'
col_time = 'time'
cols_emg = [f'EMG_{i}' for i in range(8)]
cols_emg_cal = [f'{col}_cal' for col in cols_emg]

# X (id, time, EMG data), y (hold labels)
DataSet = tuple[pd.DataFrame, pd.Series]

def get_data() -> DataSet:
    dataset = pd.read_csv(dataset_path)
    X = pd.DataFrame(dataset[[col_id, col_time, *cols_emg, *cols_emg_cal]])
    y = pd.Series(dataset[col_hold]).set_axis(dataset[col_id])
    y = pd.Series(y[~y.index.duplicated(keep='first')])
    return (X, y)

def get_feature_list():
    with open(features_path, 'r') as fp:
        return json.load(fp)
