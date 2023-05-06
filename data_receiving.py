from opcua import Client
from database import crud
from time import sleep

URL = 'opc.tcp://localhost:8001/opcua/server/'
URI = 'http://gas-turbine-power-plant'
PARAMS = crud.get_parameters_list()

client = Client(URL)

val_parameters = {}
    
try:
    client.connect()
    root = client.get_root_node()
    idx = client.get_namespace_index(URI)

    while True: # надо разобраться, что делать с бесконечным циклом
        '''

        далее идёт получение данных турбины
        в учётом информации из используемого набора данных

        '''

        # тест
        # var_temperature = root.get_child(
        #     [
        #         '0:Objects',
        #         '{}:Parameters'.format(idx),
        #         '{}:temperature'.format(idx)
        #     ]
        # )
        # print('var_temperature = ', var_temperature)
        # temperature = client.get_node(var_temperature)
        # print('temperature = ', temperature)
        # print('temperature_value = ', temperature.get_value())

        for par in PARAMS:
            var_param = root.get_child(
                [
                    '0:Objects',
                    '{}:Parameters'.format(idx),
                    '{}:{}'.format(idx, par)
                ]
            )
            val_parameters[par] = client.get_node(var_param).get_value()
            print(par, var_param, val_parameters[par])

        # внесение полученных данных в базу данных
        for par in val_parameters:

            '''

            табличные значения параметров должны будут соответствовать виду:
            название параметра из датасета_компонент турбины

            '''

            par_name, eq_name = par.split('_')
            crud.create_measuring(param_value=val_parameters[par], param_name=par_name, equip_name=eq_name)
            
        # sleep(10)

finally:
    client.disconnect()
    print('Соединение с сервером закрыто')
