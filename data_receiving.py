from opcua import Client
from database import crud
from time import sleep

URL = 'opc.tcp://localhost:8001/opcua/server/'
URI = 'http://gas-turbine-power-plant'
PARAMS = crud.get_parameters_list()

client = Client(URL)

val_parameters = {}
    
try:
    cycle = 1
      
    while True:
        client.connect()
        root = client.get_root_node()
        idx = client.get_namespace_index(URI)
        
        print('Received data:')
        for par in PARAMS:
            var_param = root.get_child(
                [
                    '0:Objects',
                    '{}:Parameters'.format(idx),
                    '{}:{}'.format(idx, par.split('_')[0])
                ]
            )
            val_parameters[par] = client.get_node(var_param).get_value()
            print(par, var_param, val_parameters[par])
            
            # внесение полученных данных в базу данных
            eq_name = par.split('_')[1]
            crud.create_measuring(param_value=val_parameters[par], param_name=par, equip_name=eq_name)
        
        print('\ncycle num:', cycle, '\n')
        cycle += 1

        sleep(5)

finally:
    client.disconnect()
    print('Соединение с сервером закрыто')
