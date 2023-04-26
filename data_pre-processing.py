import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from database import crud
from datetime import datetime
from pathlib import Path

measurings = crud.get_measurings()

columns = crud.get_parameters_list()    # список
index = set()                           # множество
data = {}.fromkeys(columns)             # словарь

for mes in reversed(measurings):
    par_id = mes['id_parameter']
    par_name = crud.get_parameter_by_id(param_id=par_id).par_name

    idx = mes['time_measuring'].strftime('%Y-%m-%d %H:%M:%S')

    val = mes['value']

    index.add(idx)
    data[par_name] = val

datetime_index = pd.DatetimeIndex(data=index)

frame = pd.DataFrame(data=data, index=datetime_index, dtype='float64')

# удаление нулевых значений
frame.dropna(inplace=True)

# нормализация данных
scaler = MinMaxScaler()
final_frame = pd.DataFrame(data=scaler.fit_transform(frame),
                           index=frame.index,
                           columns=frame.columns)

path = Path(__file__)
parent = str(path.parent.parent.absolute())
path_to_file = ''.join([parent, '\\datasets_to_predict'])

file_name = '\\dataset_{}.csv'.format(datetime.now().strftime('%Y_%m_%d_%H_%M_%S'))

final_frame.to_csv(''.join([path_to_file, file_name]))
