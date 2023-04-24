from opcua import Server

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


# старт сервера
server.start()
print(f'Server has been started at {URL}')
