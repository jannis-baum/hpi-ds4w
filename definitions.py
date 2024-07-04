import os

root_dir = os.path.dirname(os.path.realpath(__file__))

def _establish_dir(name: str) -> str:
    directory = os.path.join(root_dir, name)
    os.makedirs(directory, exist_ok=True)
    return directory

data_dir = _establish_dir('data')
model_dir = _establish_dir('model-saves')
