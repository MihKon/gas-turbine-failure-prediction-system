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

'''

далее пойдет назначение параметров турбины
согласно используемому набору данных:

температура турбины, компрессора,
выходные напряжения и мощность, ток,
вибрация и т.д.

'''
# тест
# temperature = params.add_variable(space, 'temperature', 0)
# temperature.set_writable()

for par in PARAMS:
    val_params[par] = params.add_variable(space, '{}'.format(par), 0)

# старт сервера
try:
    server.start()
    print(f'Server has been started at {URL}')

    while True:

        # print(temperature)
        # val_temperature = randint(230, 280)
        # temperature.set_value(val_temperature)
        # print(val_temperature)
        # print(temperature)

        for par in val_params:
            val_par = randint(230, 500)
            val_params[par].set_value(val_par)
            print(par, val_par, val_params[par])

        sleep(10)
finally:
    server.stop()
