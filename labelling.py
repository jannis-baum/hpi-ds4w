import os

import pandas as pd

if __name__ == '__main__':
    data_dir = 'data'

    for day_name in os.listdir(data_dir):
        day_path = os.path.join(data_dir, day_name)
        if not os.path.isdir(day_path): continue
        
        for recording in os.listdir(day_path):
            recording_path = os.path.join(day_path, recording)
            if not os.path.isdir(recording_path): continue
            
            bounds_path = os.path.join(recording_path, 'frame_boundaries.csv')
            data_path = os.path.join(recording_path, 'data.csv')
            if not os.path.exists(bounds_path):
                print(f'Frame boundary definitions for {recording_path} missing, skipping.')
                continue
            with open(bounds_path, 'r') as fp:
                bounds = pd.read_csv(fp)
            with open(data_path, 'r') as fp:
                data = pd.read_csv(fp)
            
            aggregated = pd.DataFrame(columns=[*data.columns, 'hold', 'rep'])

            for i, row in bounds.iterrows():
                condition = (data['frame'] >= row['frame_start']) & (data['frame'] <= row['frame_end'])
                aggregated.loc[len(aggregated)] = [*data[condition].mean(), row['hold'], i]

            aggregated.to_csv(os.path.join(recording_path, 'data_labelled.csv'), index=False)
