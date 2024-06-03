import os

import pandas as pd

data_dir = 'data'
dataset_path = os.path.join(data_dir, 'dataset.csv')
emg_cols = [f'EMG_{i}' for i in range(8)]
emg_cols_cal = [f'{col}_cal' for col in emg_cols]

DataSet = tuple[pd.DataFrame, pd.DataFrame]

# get data for 1 person on 1 date
def read_labelled(person: str, date: str) -> DataSet:
    path = os.path.join(data_dir, date, person, 'data_labelled.csv')
    with open(path, 'r') as fp:
        data_raw = pd.read_csv(fp)

    X = pd.DataFrame(data_raw[[f'EMG{i}' for i in range(8)]])
    y = pd.DataFrame(data_raw[['hold', 'rep']])
    y['name'] = [person] * len(data_raw)
    y['date'] = [date] * len(data_raw)
    return X, y

# get concatenated data for multiple people/dates
def get_data(people: list[str] | None = None, dates: list[str] | None = None) -> DataSet:
    data_sets = list[DataSet]()

    for date in os.listdir(data_dir):
        date_path = os.path.join(data_dir, date)
        if not os.path.isdir(date_path) or (dates is not None and date not in dates): continue

        for person in os.listdir(date_path):
            if people is not None and person not in people: continue
            try:
                data_sets.append(read_labelled(person, date))
            except: continue

    return tuple(pd.concat(col).reset_index(drop=True) for col in zip(*data_sets)) # type: ignore
