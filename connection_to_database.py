import psycopg2
import sys
import tensorflow as tf
import numpy as np
from database import crud

# в общем-то тестовый файл для проверки работы с базой данных
DATABASE_URL = 'postgresql://mihkon:postgres@localhost:5432/diplomadbv2'

'''
class Connection():

    def __init__(self):
        
        connection = None
        cursor = None

        try:
            connection = psycopg2.connect(DATABASE_URL)
            print('Соединение с базой данных установлено')
            cursor = connection.cursor()
        except:
            print('Не удалось установить соединение с базой данных')
        
        self.database_url = DATABASE_URL
        self.connection = connection
        self.cursor = cursor
    

    def __del__(self):
        self.connection.close()
        self.cursor.close()
        print('Соединение с базой данных закрыто')


    def get_table_values(self, table):
        pass


try:
    connection = psycopg2.connect(DATABASE_URL)
    print('Ура! Работает!')
    cursor = connection.cursor()

    # sql_query = 'SELECT * FROM parameters;'
    # cursor.execute(sql_query)
    # print('Данные таблицы параметров:\n',cursor.fetchall())
finally:
    cursor.close()
    connection.close()
    print('Соединение с базой данных закрыто')
'''
'''
# parameters = crud.get_parameters()
# print(parameters)
# # print([par.par_name for par in parameters])
# for par in parameters:
#     print(par)

# param = crud.get_parameter_by_name('Расход жидкого топлива')
# print(param.id_parameter, param.par_name)
# measurings = crud.get_measurings()
# print(len(measurings))
# for m in measurings:
#     print(m)
# crud.create_measuring(param_id=7, equip_id=2, param_value=7.4)
# measurings = crud.get_measurings()
# print(len(measurings))
# for m in measurings:
#     print(m)

# predicts = crud.get_predicts()
# for predict in predicts:
#     print(predict)

# params = crud.get_parameters_list()
# print(params)
'''


def set_layer_weights(weight, lr_name, idx, model):
    if type(weight) is np.ndarray:
        for wght in weight:
            idx = set_layer_weights(wght, lr_name, idx, model)
    else:
        title = '{}_w{}'.format(lr_name, idx)
        crud.create_predict_params(title, weight, model)
        idx += 1
    
    return idx


path_to_file = 'C:\\Users\\miha-\\Desktop\\diplom_program\\models\\Compressor T5 average_24.h5'
param = path_to_file.split('\\')[-1].split('_')[0]
model_title = path_to_file.split('\\')[-1]
print(param)
# crud.create_model(1, model_title, path_to_file, stnd_par_name=param)

model = tf.keras.models.load_model(path_to_file)
model_id = crud.get_model_by_title(model_title).id_model

for lr in model.layers:
    idx = 1
    for w in lr.get_weights():
        set_layer_weights(w, lr.name, idx, model_id)
