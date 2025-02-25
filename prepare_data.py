import os

import pandas as pd

from definitions import data_dir
from script.dataset import (
    col_hold,
    col_id,
    col_time,
    cols_emg,
    cols_emg_cal,
    dataset_path,
)

# anonymize people's names to integers
_person2int = dict[str, int]()
def _anonymize(person: str) -> int:
    if person in _person2int:
        return _person2int[person]
    else:
        new_id = len(_person2int)
        _person2int[person] = new_id
        return new_id

# read frame boundaries file from csv or xlsx
def _get_frame_boundaries(recording_path: str) -> pd.DataFrame:
    for extension, reader in [('csv', pd.read_csv), ('xlsx', pd.read_excel)]:
        bounds_path = os.path.join(recording_path, f'frame_boundaries.{extension}')
        if os.path.exists(bounds_path):
            return reader(bounds_path)
    raise Exception(f'Frame boundary definitions for {recording_path} missing')

# get values within row from bounds file
def _get_data(bounds, data) -> tuple[str, pd.DataFrame]:
    condition = (data['frame'] >= bounds['frame_start']) & (data['frame'] <= bounds['frame_end'])
    return (bounds['label'], data.loc[condition, cols_emg])

if __name__ == '__main__':
    dataset = pd.DataFrame(columns=[
        col_hold,         # climbing hold
        col_id,           # unique set identifier: {date}_{person}_{recording-i}_{set-i}
        col_time,         # time stamp for set
        *cols_emg,      # absolute sensor data
        *cols_emg_cal,  # calibrated sensor data
    ])

    for day_name in os.listdir(data_dir):
        day_path = os.path.join(data_dir, day_name)
        if not os.path.isdir(day_path): continue

        # get day & recording index
        recording_components = day_name.split('-')
        day = recording_components[0]
        recording = int(recording_components[1]) if len(recording_components) > 1 else '1'

        for person in os.listdir(day_path):
            recording_path = os.path.join(day_path, person)
            if not os.path.isdir(recording_path): continue
            person_id = f'p{_anonymize(person)}'

            try:
                bounds = _get_frame_boundaries(recording_path)
            except Exception as e:
                print(f'Error: {", ".join(e.args)}, skipping')
                continue

            data_path = os.path.join(recording_path, 'data.csv')
            with open(data_path, 'r') as fp:
                data = pd.read_csv(fp)

            if 'calibration' not in list(bounds['label']):
                print(f'Calibration period missing for {recording_path}, skipping.')
                continue

            calibration = _get_data(bounds[bounds['label'] == 'calibration'].iloc[0], data)[1].mean()
            set_index = 1
            for _, row in bounds.iterrows():
                if row['label'] == 'calibration': continue

                hold, values = _get_data(row, data)
                values[col_hold] = hold
                values[col_id] = f'{day}_{person_id}_{recording}_{set_index}'
                values[col_time] = values.reset_index().index
                values[cols_emg_cal] = values[cols_emg] - calibration

                # reorder columns and concat with existing data
                values = values[dataset.columns]
                if dataset.empty:
                    dataset = values
                else:
                    dataset = pd.concat([dataset, values])

                set_index += 1

    dataset.to_csv(dataset_path, index=False)
