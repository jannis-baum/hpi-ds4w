import pandas as pd

from script.helpers import get_data

if __name__ == '__main__':
    X, y = get_data()
    df = pd.concat([X, y], axis=1)
    df.to_csv('data/aggregated.csv')
