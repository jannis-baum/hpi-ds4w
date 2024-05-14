import os
import time

from IPython.display import Markdown, display
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.metrics import accuracy_score


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
DataSet = tuple[pd.DataFrame, pd.Series, pd.Series]

# get data for 1 person on 1 date
def read_labelled(person: str, date: str) -> DataSet:
    path = os.path.join(__data_dir, date, person, 'data_labelled.csv')
    with open(path, 'r') as fp:
        data_raw = pd.read_csv(fp)

    X = pd.DataFrame(data_raw[[f'EMG{i}' for i in range(8)]])
    holds = pd.Series(data_raw['hold'])
    names = pd.Series([person] * len(holds))
    return X, holds, names

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

# ------------------------------------------------------------------------------
# MARK: evaluation -------------------------------------------------------------

def report_cm(title, y_true, y_pred, classifier):
    display(Markdown(f'# {title}'))
    print(f'accuracy: {accuracy_score(y_true, y_pred)}')
    ConfusionMatrixDisplay.from_predictions(
        y_true, y_pred,
        labels=classifier.classes_,
        normalize='true',
        xticks_rotation='vertical'
    )
    plt.show()
