import os
import glob
import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from pathlib import Path
from database import crud
from collections import defaultdict

BATCH_SIZE = 8
scaler = MinMaxScaler()


def get_current_dataset():
    
    dataset_file = ''

    path = Path(__file__)
    parent = str(path.parent.parent.absolute())
    path_to_file = ''.join([parent, '\\datasets_to_predict'])

    files = glob.glob(path_to_file + '\\' + '*.csv')
    if files:
        files = sorted(files, key=os.path.getctime)
        dataset_file = files[0]
    
    return dataset_file


def predict_params(data, parameter, predict_lst, hours):

    model_title = ''.join([parameter, '_{}.h5'.format(hours)])
    
    try:
        model_path = crud.get_model_by_title(model_title).path_to_file
        print('Модель найдена!', model_path)
    except:
        print('Модель для данного параметра не найдена!', parameter)
        return
    
    predict_model = tf.keras.models.load_model(model_path)

    # код не будет работать с этого момента, пока нет модели с нормальным форматом данных
    #try:
    x = np.expand_dims(data.values, axis=0)
    # x = tf.data.Dataset.from_tensors(data.values)
    # x.batch(BATCH_SIZE)
    param_pred = predict_model.predict(x)
    pred_res = scaler.inverse_transform(param_pred)
    print(param_pred, '\n', pred_res)
    predict_lst[parameter].append(pred_res)
    #except ValueError:
        #print('Неверный формат данных')
    
    return predict_lst


def predict_verdict():
    pass


dataset = get_current_dataset()
data = pd.read_csv(dataset)

predicts_24h = defaultdict(list)
# predicts_72h = defaultdict(list)

# datarows = data.to_dict('records')
for parameter in data.columns:
    predicts_24h = predict_params(data, parameter, predicts_24h, '24')
    # predicts_72h = predict_params(row, predicts_72h, '72')
