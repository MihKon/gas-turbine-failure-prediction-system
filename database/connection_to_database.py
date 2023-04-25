import psycopg2
import crud
import sys

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

predicts = crud.get_predicts()
for predict in predicts:
    print(predict)