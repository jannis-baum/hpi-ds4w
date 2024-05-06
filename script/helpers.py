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
# MARK: ugly data loading functions --------------------------------------------

# get data for 1 person on 1 day
def get_data_1p(person: str, date: str = '0423'):
    path = f'data/{date}/{person}-hangboard/data_labelled.csv'
    with open(path, 'r') as fp:
        data_raw = pd.read_csv(fp)

    X = data_raw[[f'EMG{i}' for i in range(8)]]
    holds = data_raw['hold'] + '_' + data_raw['details']
    names = pd.Series([person] * len(holds))
    return X, holds, names

# get concatenated data for multiple people on 1 day
def get_data(people: list[str] = ['jonas', 'gregor', 'nikolai', 'jannis'], date: str = '0423'):
    return (
        pd.concat(col).reset_index(drop=True) for col in zip(*[
            get_data_1p(name, date) for name in people
        ])
    )

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
