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

            # get bounds as csv or xlsx
            bounds: None | pd.DataFrame = None
            for extension, reader in [('csv', pd.read_csv), ('xlsx', pd.read_excel)]:
                bounds_path = os.path.join(recording_path, f'frame_boundaries.{extension}')
                if os.path.exists(bounds_path):
                    bounds = reader(bounds_path)
                    break
            if bounds is None:
                print(f'Frame boundary definitions for {recording_path} missing, skipping.')
                continue

            data_path = os.path.join(recording_path, 'data.csv')
            with open(data_path, 'r') as fp:
                data = pd.read_csv(fp)

            aggregated = pd.DataFrame(columns=[*data.columns, 'hold', 'rep'])

            for i, row in bounds.iterrows():
                condition = (data['frame'] >= row['frame_start']) & (data['frame'] <= row['frame_end'])
                aggregated.loc[len(aggregated)] = [*data[condition].mean(), row['label'], i]

            if 'calibration' not in list(aggregated.hold):
                print(f'Calibration period missing for {recording_path}, skipping.')
                continue

            calibration = aggregated[aggregated.hold == 'calibration'].iloc[0]
            for h in range(7):
                sensor = f'EMG{h}'
                aggregated[f'{sensor}_cal'] = aggregated[sensor] / calibration[sensor]

            aggregated.drop(aggregated[aggregated.hold == 'calibration'].index, inplace=True)
            aggregated.to_csv(os.path.join(recording_path, 'data_labelled.csv'), index=False)
