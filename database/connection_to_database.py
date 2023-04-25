import psycopg2
from database import crud

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

parameters = crud.get_parameters()
print(parameters)