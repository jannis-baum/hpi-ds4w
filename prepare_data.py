import os

import pandas as pd

from script.dataset import data_dir, dataset_path, emg_cols, emg_cols_cal

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

# get means for values within row from bounds file
def _get_means(bounds, data) -> tuple[str, pd.Series]:
    condition = (data['frame'] >= bounds['frame_start']) & (data['frame'] <= bounds['frame_end'])
    return (bounds['label'], data.loc[condition, emg_cols].mean())

if __name__ == '__main__':
    dataset = pd.DataFrame(columns=[
        'person',       # anonymized person identifier
        'date',         # recording date
        'recording',    # recording index for given date
        'set',          # set index in given recording
        'hold',         # climbing hold
        *emg_cols,      # absolute sensor data
        *emg_cols_cal,  # calibrated sensor data
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
            person_id = _anonymize(person)

            try:
                bounds = _get_frame_boundaries(recording_path)
            except Exception as e:
                print(f'Error: {", ".join(e.args)}, skipping')
                continue

            data_path = os.path.join(recording_path, 'data.csv')
            with open(data_path, 'r') as fp:
                data = pd.read_csv(fp)

            aggregated = pd.DataFrame(columns=[*data.columns, 'hold', 'rep'])


            if 'calibration' not in list(bounds['label']):
                print(f'Calibration period missing for {recording_path}, skipping.')
                continue

            _, calibration = _get_means(bounds[bounds['label'] == 'calibration'].iloc[0], data)
            set_index = 1
            for _, row in bounds.iterrows():
                if row['label'] == 'calibration': continue

                hold, means = _get_means(row, data)
                dataset.loc[len(dataset)] = [
                    person_id,
                    day,
                    recording,
                    set_index,
                    hold,
                    *means,
                    *list(means - calibration)
                ]
                set_index += 1

    dataset.to_csv(dataset_path)
