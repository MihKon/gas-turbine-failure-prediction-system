from opcua import Client

URL = 'opc.tcp://localhost:8001/opcua/server/'
URI = 'http://gas-turbine-power-plant'

if __name__ == '__main__':

    client = Client(URL)
    
    try:
        client.connect()
        root = client.get_root_node()
        idx = client.get_namespace_index(URI)
        while True:
            '''

            далее идёт получение данных турбины
            в учётом информации из используемого набора данных

            '''

            # тест
            var_temperature = root.get_child(
                [
                    '0:Objects',
                    '{}:Parameters'.format(idx),
                    '{}:temperature'.format(idx)
                ]
            )
            print('var_temperature = ', var_temperature)
            temperature = client.get_node(var_temperature)
            print('temperature = ', temperature)
            print('temperature_value = ', temperature.get_value())

        # внесение полученных данных в базу данных
        

    finally:
        client.disconnect()
        print('Соединение с сервером закрыто')

