from opcua import Server
from time import sleep
from random import randint

URL = 'opc.tcp://localhost:8001/opcua/server/'
URI = 'http://gas-turbine-power-plant'

server = Server()

server.set_endpoint(URL)
server.set_server_name('OPC UA SIMULATION SERVER')

space = server.register_namespace(URI)

node = server.get_objects_node()

params = node.add_object(space, 'Parameters')

'''

далее пойдет назначение параметров турбины
согласно используемому набору данных:

температура турбины, компрессора,
выходные напряжения и мощность, ток,
вибрация и т.д.

'''
# тест
temperature = params.add_variable(space, 'temperature', 0)
temperature.set_writable()

# старт сервера
try:
    server.start()
    print(f'Server has been started at {URL}')

    while True:
        print(temperature)
        val_temperature = randint(230, 280)
        temperature.set_value(val_temperature)
        print(val_temperature)
        print(temperature)
        sleep(10)
finally:
    server.stop()
