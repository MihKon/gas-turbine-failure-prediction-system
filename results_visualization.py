import os
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
from database import crud

PREDICTS_DIRECTORY = ''.join([str(Path(__file__).parent.parent.absolute()), '\\predicts'])
IMAGE_DIRECTORY = ''.join([str(Path(__file__).parent.parent.absolute()), '\\predict_images'])

print(IMAGE_DIRECTORY)


def get_current_predict():
    dataset_file = ''

    files = os.listdir(PREDICTS_DIRECTORY)
    if files:
        lst_files = [os.path.join(PREDICTS_DIRECTORY, file) for file in files]
        files = [file for file in lst_files if os.path.isfile(file)]
        dataset_file = max(files, os.path.getctime)
    
    return dataset_file


def plot_predicts(param_row):
    plt.plot(param_row)
    pass

predicts = get_current_predict()
pred_frame = pd.read_csv(predicts)

for pred in predicts.columns:
    pass


