import pandas as pd
from collections import defaultdict
from database import crud
from datetime import datetime
from pathlib import Path

PAST = 24
measurings = crud.get_measurings(PAST)

data = defaultdict(list) # словарь списков

for mes in reversed(measurings):
    par_id = mes['id_parameter']
    par_name = crud.get_parameter_by_id(param_id=par_id).par_name.split('_')[0]

    val = mes['value']

    data[par_name].append(val)


frame = pd.DataFrame(data=data, dtype='float64')

# удаление нулевых значений
frame.dropna(inplace=True)

path = Path(__file__)
parent = str(path.parent.parent.absolute())
directory = ''.join([parent, '\\datasets_to_predict'])
file_name = '\\dataset_{}.csv'.format(datetime.now().strftime('%Y_%m_%d_%H_%M_%S'))
path_to_file = ''.join([directory, file_name])

frame.to_csv(path_to_file, index=False)