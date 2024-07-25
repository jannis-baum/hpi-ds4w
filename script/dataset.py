import os

import numpy.typing as npt
import pandas as pd
from sklearn.model_selection import KFold

from definitions import data_dir

dataset_path = os.path.join(data_dir, 'dataset.csv')

col_hold = 'hold'
# id is '{day}_{person_id}_{recording}_{set_index}'
col_id = 'id'
col_time = 'time'
cols_emg = [f'EMG_{i}' for i in range(8)]
cols_emg_cal = [f'{col}_cal' for col in cols_emg]

# X (id, time, EMG data), y (hold labels)
DataSet = tuple[pd.DataFrame, pd.Series]

def get_data(simplify: bool = True) -> DataSet:
    dataset = pd.read_csv(dataset_path)
    X = pd.DataFrame(dataset[[col_id, col_time, *cols_emg, *cols_emg_cal]])
    y = pd.Series(dataset[col_hold]).set_axis(dataset[col_id])
    y = pd.Series(y[~y.index.duplicated(keep='first')])

    if simplify:
        hold_mapping = {
            'crimp_45': 'crimp',
            'crimp_20': 'crimp',
            'jug': 'sloper_jug',
            'sloper_30': 'sloper_jug'
        }
        y = y.map(hold_mapping)

    return (X, y)

# extract information from id column
def get_id_col(X: pd.DataFrame, col) -> pd.Series:
    return X['id'].str.split('_', expand=True)[col]

# split data into train/test and create folds for tests
class SplitDataset:
    def __init__(
        self,
        # data and labels should both either be pandas or numpy
        data: pd.DataFrame | npt.NDArray, labels: pd.Series | npt.NDArray,
        participants: pd.Series, test_p: str = 'p1',
        n_folds: int = 5, random_state: int = 42
    ):
        split = participants == test_p

        self._data_train, self._data_test = data[~split], data[split]
        self._labels_train, self._labels_test = labels[~split], labels[split]

        self.n_folds = n_folds
        kf = KFold(n_splits=self.n_folds, random_state=random_state, shuffle=True)
        self._folds = list(kf.split(self._data_train))

    # get data from pandas DataFrame or Series or numpy array
    def _get_data(self, data: pd.DataFrame | pd.Series | npt.NDArray, idx):
        if isinstance(data, pd.DataFrame) or isinstance(data, pd.Series):
            return data.iloc[idx]
        return data[idx]

    # get folded training data
    def get_train(self) -> list[tuple]:
        return [
            (lambda idx_train:
                (self._get_data(self._data_train, idx_train), self._get_data(self._labels_train, idx_train))
            )(self._folds[fold][0])
        for fold in range(self.n_folds)]

    def get_test(self) -> tuple:
        return (self._data_test, self._labels_test)
