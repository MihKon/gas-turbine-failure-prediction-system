import os
import pandas as pd
from pathlib import Path
from database import crud, models

MODELS = crud.get_models()
PARAMS = list(map(lambda x: x.split('_')[0], crud.get_parameters_list())) 


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


def predict_params(row, predict_lst, hours):

    for param, val in row.items():
        predict_model = crud.get_model_by_title(''.join([param, '_{}H'.format(hours)]))
        param_pred = predict_model.predict(val)
        predict_lst.update([(param, param_pred)])
    
    return predict_lst


def predict_verdict():
    pass


dataset = get_current_dataset()
data = pd.read_csv(dataset)

predicts_24h = {}.fromkeys(PARAMS)
predicts_72h = {}.fromkeys(PARAMS)

datarows = data.to_dict('records')
for row in datarows:
    predicts_24h = predict_params(row, predicts_24h, '24')
    predicts_72h = predict_params(row, predicts_72h, '72')
