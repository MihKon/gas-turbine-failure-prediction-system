import pandas as pd
from opcua import Server
from time import sleep
from random import randint
from database.crud import get_parameters_list

URL = 'opc.tcp://localhost:8001/opcua/server/'
URI = 'http://gas-turbine-power-plant'
PARAMS = get_parameters_list()

server = Server()

server.set_endpoint(URL)
server.set_server_name('OPC UA SIMULATION SERVER')

space = server.register_namespace(URI)

node = server.get_objects_node()

params = node.add_object(space, 'Parameters')
val_params = {}
test_params = pd.read_csv(r'C:\Users\miha-\Desktop\diplom_program\programs\test_datasets\test_dataset1.csv')\
    .to_dict().keys()

for par in test_params:
    par_name = par.split('_')[0]
    val_params[par_name] = params.add_variable(space, '{}'.format(par), 0)
    val_params[par_name].set_writable()

test_data = pd.read_csv(r'C:\Users\miha-\Desktop\diplom_program\programs\test_datasets\test_dataset1.csv')\
    .to_dict('records')

# старт сервера
try:
    server.start()
    print(f'Server is running at {URL}')

    #while True:
    for idx in range(len(test_data[:5])):
        
        for par in val_params:
            val_par = test_data[idx][par]
            val_params[par].set_value(val_par)
            print(par, val_par, val_params[par])

        print('\n', 'cycle_num:', idx)
        sleep(10)

finally:
    server.stop()
