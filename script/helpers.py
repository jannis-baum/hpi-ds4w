import os
import time

import pandas as pd

# ------------------------------------------------------------------------------
# MARK: data recording stuff ---------------------------------------------------

def _current_time():
    return round(time.time() * 1000)

_initial_time = _current_time()

# milliseconds since startup
def millis():
    return _current_time() - _initial_time

# ------------------------------------------------------------------------------
# MARK: data loading functions -------------------------------------------------

__data_dir = 'data'
DataSet = tuple[pd.DataFrame, pd.DataFrame]

# get data for 1 person on 1 date
def read_labelled(person: str, date: str) -> DataSet:
    path = os.path.join(__data_dir, date, person, 'data_labelled.csv')
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

    for date in os.listdir(__data_dir):
        date_path = os.path.join(__data_dir, date)
        if not os.path.isdir(date_path) or (dates is not None and date not in dates): continue

        for person in os.listdir(date_path):
            if people is not None and person not in people: continue
            try:
                data_sets.append(read_labelled(person, date))
            except: continue

    return tuple(pd.concat(col).reset_index(drop=True) for col in zip(*data_sets)) # type: ignore
