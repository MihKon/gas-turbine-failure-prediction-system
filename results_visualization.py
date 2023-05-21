import os
import glob
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime


DATASET_DIRECTORY = ''.join([str(Path(__file__).parent.parent.absolute()), '\\datasets_to_predict'])
PREDICTS_DIRECTORY = ''.join([str(Path(__file__).parent.parent.absolute()), '\\predicts'])
IMAGE_DIRECTORY = ''.join([str(Path(__file__).parent.parent.absolute()), '\\predicts_images'])


def get_current_file(directory):
    dataset_file = ''

    files = glob.glob(directory + '\\' + '*.csv')
    if files:
        files = sorted(files, key=os.path.getctime)
        dataset_file = files[-1]
    
    return dataset_file


def create_time_steps(length):
  return list(range(-length, 0))


def plot_predicts(predict_data, past_data, param):
    fig, ax = plt.subplots()
    fig.set_size_inches(50, 15)

    n_past = create_time_steps(len(past_data))
    n_target = len(predict_data)

    ax.plot(n_past, past_data,
             label='Данные наблюдаемого периода',
             color='steelblue', marker='.')
    
    ax.plot(np.arange(n_target),
             predict_data,
             color='orange', marker='.',
             label='Предсказанные значения прогнозируемого периода'.format(param))
    
    ax.set_title('Прогнозирование показаний параметра {}'.format(param), size=25)
    ax.set_ylabel('Значение', size=22)
    ax.set_xlabel('Периоды, час', size=22)

    x_start, x_end = (int(axe) for axe in ax.get_xlim())
    ax.xaxis.set_ticks(np.arange(x_start, x_end, 2))

    y_start, y_end = (int(axe) for axe in ax.get_ylim())
    ax.yaxis.set_ticks(np.arange(y_start, y_end, 30))

    ax.legend(loc='upper left')
    ax.grid(which='both')
    ax.minorticks_on()
    ax.tick_params(which='minor', bottom=False, left=False)

    plt.xticks(size=18)
    plt.yticks(size=22)
    
    directory_to_save = ''.join(
        [
            IMAGE_DIRECTORY,
            '\\{}'.format(datetime.now().strftime('%Y_%m_%d_%H_%M_%S'))
        ]
    )

    if not os.path.exists(directory_to_save):
        os.makedirs(directory_to_save)

    path_to_save = ''.join([directory_to_save, '\\{}_predict.png'.format(param)])
    fig.savefig(path_to_save, bbox_inches='tight')
    
    # plt.show()


predicts = get_current_file(PREDICTS_DIRECTORY)
pred_frame = pd.read_csv(predicts)
pred_frame.dropna(axis=1, inplace=True)
print(pred_frame)

data = get_current_file(DATASET_DIRECTORY)
dataframe = pd.read_csv(data)
print(dataframe)

for param in pred_frame.columns:
    plot_predicts(pred_frame[param].values, dataframe[param].values, param)
