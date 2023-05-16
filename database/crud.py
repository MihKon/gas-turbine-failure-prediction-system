from . import models
from datetime import datetime


PARAMS_NUM = len(models.Parameters.select())


def get_equipment():
    return models.Equipment.select().order_by(
        models.Equipment.id_equipment
    ).dicts()


def get_equipment_by_name(eq_name: str):
    return models.Equipment.get(models.Equipment.equip_name == eq_name)


def get_parameters():
    return models.Parameters.select().order_by(
        models.Parameters.id_parameter
    ).dicts()


def get_parameter_by_name(param_name: str):
    return models.Parameters.get(models.Parameters.par_name == param_name)


def get_parameter_by_id(param_id: int):
    return models.Parameters.get(models.Parameters.id_parameter == param_id)


def get_parameters_list():
    parameters = []

    params = get_parameters()
    for par in params:
        parameters.append(par['par_name'])

    return parameters


def get_parameter_by_part_name(name: str):
    params = get_parameters_list()
    par_name = ''

    for par in params:
        if par.split('_')[0] == name:
            par_name = par

    return get_parameter_by_name(par_name)


def get_measurings(limit: int = 1):
    return models.Measurings.select().limit(PARAMS_NUM*limit).order_by(
        models.Measurings.id_measuring.desc()
    ).dicts()


def get_measuring_by_par(param_id: int = None,
                         par_name: str = None):
    
    if param_id is None and par_name is not None:
        param_id = get_parameter_by_part_name(par_name).id_parameter

    measurings = models.Measurings.select().where(
        models.Measurings.id_parameter == param_id
    ).order_by(models.Measurings.time_measuring.desc()).limit(1)

    measuring = measurings[-1]

    return measuring


def create_measuring(param_value: float,
                     param_id: int = None,
                     param_name: str = None,
                     equip_id: int = None,
                     equip_name: str = None):
    
    if param_id is None and param_name is not None:
        param_id = get_parameter_by_name(param_name=param_name).id_parameter

    if equip_id is None and equip_name is not None:
        equip_id = get_equipment_by_name(eq_name=equip_name).id_equipment
    
    measuring_time = datetime.now()
    
    models.Measurings.create(
        id_parameter=param_id,
        id_equipment=equip_id,
        time_measuring=measuring_time,
        value=param_value
    )


def get_stnd_params():
    return models.StandardParams.select().order_by(
        models.StandardParams.id_standard_parameter
    ).dicts()


def get_stnd_par_by_name(name: str):
    return models.StandardParams.get(models.StandardParams.param_name == name)


def get_models():
    return models.Models.select().order_by(
        models.Models.id_model
    ).dicts()


def get_model_by_title(title: str):
    return models.Models.get(models.Models.title == title)


def create_model(id: int,
                 title: str,
                 path: str,
                 id_stnd_par: id = None,
                 stnd_par_name: str = None):
    if id_stnd_par is None and stnd_par_name is not None:
        id_stnd_par = get_stnd_par_by_name(stnd_par_name).id_standard_parameter
    
    models.Models.create(
        id_model=id,
        title=title,
        path_to_file=path,
        id_standard_parameter=id_stnd_par
    )


def get_predict_params():
    return models.PredictParams.select().order_by(
        models.PredictParams.id_predict_param
    ).dicts()


def create_predict_params(title: str,
                          value: float,
                          model_id: int):
    
    models.PredictParams.create(
        param_title=title,
        param_value=value,
        id_model=model_id
    )


def get_predicts():
    return models.Predicts.select().order_by(
        models.Predicts.id_predict.desc()
    ).dicts()


def create_predict(verd: int,
                   measur_id: int,
                   param_id: int = None,
                   param_name: str = None,
                   model_id: int = None,
                   model_title: str = None):
    
    if param_id is None and param_name is not None:
        param_id = get_parameter_by_part_name(param_name).id_parameter

    if model_id is None and model_title is not None:
        model_id = get_model_by_title(model_title).id_model

    models.Predicts.create(
        predict_time=datetime.now(),
        deviation=0,
        verdict=verd,
        id_measuring=measur_id,
        id_parameter=param_id,
        id_model=model_id
    )
