from opcua import Client

URL = 'opc.tcp://localhost:8001/opcua/server/'
URI = 'http://gas-turbine-power-plant'

if __name__ == '__main__':

    client = Client(URL)
    
    try:
        client.connect()
        root = client.get_root_node()

        idx = client.get_namespace_index(URI)

        '''

        далее идёт получение данных турбины
        в учётом информации из используемого набора данных

        '''

        # внесение полученных данных в базу данных
        

    finally:
        client.disconnect()
        print('Соединение с сервером закрыто')

