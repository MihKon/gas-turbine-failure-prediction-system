import os
import glob
import pandas as pd
import numpy as np
import tensorflow as tf
from pathlib import Path
from datetime import datetime
from sklearn.preprocessing import MinMaxScaler
from database import crud


def get_current_dataset():
    
    dataset_file = ''

    path = Path(__file__)
    parent = str(path.parent.parent.absolute())
    path_to_file = ''.join([parent, '\\datasets_to_predict'])

    files = glob.glob(path_to_file + '\\' + '*.csv')
    if files:
        files = sorted(files, key=os.path.getctime)
        dataset_file = files[-1]
    
    return dataset_file


def prepare_dataset(frame):

    scalers = {}.fromkeys(frame.columns)
    scaler = MinMaxScaler()

    final_frame = pd.DataFrame(data=scaler.fit_transform(frame),
                               index=frame.index,
                               columns=frame.columns)
    
    for col in frame.columns:
        val = frame[col].values.reshape(-1, 1)
        scalers[col] = MinMaxScaler().fit(val)
    
    return final_frame, scalers


def predict_params(data, parameter, hours, scaler):
    
    model_title = ''.join([parameter, '_{}.h5'.format(hours)])
    
    try:
        model_path = crud.get_model_by_title(model_title).path_to_file
        print('Модель найдена!', model_path)
    except:
        print('Модель для данного параметра не найдена', parameter)
        return
    
    predict_model = tf.keras.models.load_model(model_path)

    x = np.expand_dims(data.values, axis=0)
    param_pred = predict_model.predict(x)
    pred_res = scaler.inverse_transform(param_pred.reshape(-1, 1))
    
    return pred_res.reshape(-1)


def predict_verdict():
    pass


dataset = get_current_dataset()
data = pd.read_csv(dataset)
data, mnmx_scalers = prepare_dataset(data)

predicts_24h = {}.fromkeys(data.columns)

for parameter in data.columns:
    param_predict = predict_params(data, parameter, '24', mnmx_scalers[parameter])
    predicts_24h[parameter] = param_predict

for par, val in predicts_24h.items():
    if predicts_24h[par] is not None:
        for v in val:
            measure_id = crud.get_measuring_by_value_and_par(v, par)
            par_id = crud.get_parameter_by_part_name(par).id_parameter
            model_id = crud.get_model_by_title('{}_24.h5'.format(par)).id_model
            crud.create_predict(v, 50, measure_id, par_id, model_id)

pred_frame = pd.DataFrame(predicts_24h)
pred_frame.to_csv('C:\\Users\\miha-\\Desktop\\diplom_program\\programs\\predicts\predict_dataset_{}.csv'\
                  .format(datetime.now().strftime('%Y_%m_%d_%H_%M_%S')), index=False)
