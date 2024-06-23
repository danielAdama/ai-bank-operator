import pathlib

def load_file(path: pathlib.Path):
    with open(str(path), 'r') as file:
        return file.read()