import pandas as pd
from opcua import Server
from pathlib import Path
from time import sleep
from random import randint
from database.crud import get_parameters_list

URL = 'opc.tcp://localhost:8001/opcua/server/'
URI = 'http://gas-turbine-power-plant'
PARAMS = get_parameters_list()
PAST = 72

server = Server()

server.set_endpoint(URL)
server.set_server_name('OPC UA SIMULATION SERVER')

space = server.register_namespace(URI)

node = server.get_objects_node()

params = node.add_object(space, 'Parameters')
val_params = {}

path = Path(__file__)
parent = str(path.parent.parent.absolute())
path_to_file = ''.join([parent, '\\test_datasets\\test_dataset2.csv'])

test_params = pd.read_csv(path_to_file).to_dict().keys()

for par in test_params:
    par_name = par.split('_')[0]
    val_params[par_name] = params.add_variable(space, '{}'.format(par), 0)
    val_params[par_name].set_writable()

test_data = pd.read_csv(path_to_file).to_dict('records')

# старт сервера
try:
    server.start()
    print(f'Server is running at {URL}')

    # while True:
    for idx in range(PAST, PAST+24+1):
        
        for par in val_params:
            val_par = test_data[-idx][par]
            val_params[par].set_value(val_par)
            print(par, val_par, val_params[par])

        print('\n', 'cycle_num:', idx)
        sleep(5.3)

except:
    server.stop()
    print('Сервер закрыт')

finally:
    server.stop()
    print('Сервер закрыт')
