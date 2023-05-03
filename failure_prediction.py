import os
from pathlib import Path
from database import crud


def get_current_dataset():
    
    dataset_file = ''

    path = Path(__file__)
    parent = str(path.parent.parent.absolute())
    path_to_file = ''.join([parent, '\\datasets_to_predict'])

    files = os.listdir(path_to_file)
    if files:
        lst_files = [os.path.join(path_to_file, file) for file in files]
        files = [file for file in lst_files if os.path.isfile(file)]
        dataset_file = max(files, os.path.getctime)
    
    return dataset_file


dataset = get_current_dataset()
# params = list(map(lambda x: x.split(' ')[0], crud.get_parameters_list()))
# print(params)