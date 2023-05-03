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


def get_measurings(limit: int = PARAMS_NUM):
    return models.Measurings.select().limit(limit).order_by(
        models.Measurings.id_measuring.desc()
    ).dicts()


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


def get_predicts():
    return models.Predicts.select().order_by(
        models.Predicts.id_predict.desc()
    ).dicts()


def create_predict(verd: int,
                   infl: int,
                   measur_id: int,
                   param_id: int,
                   model_id: int):

    models.Predicts.create(
        predict_time=datetime.now(),
        deviation=0,
        verdict=verd,
        influence=infl,
        id_measuring=measur_id,
        id_parameter=param_id,
        id_model=model_id
    )


def get_models():
    return models.Models.select().order_by(
        models.Models.id_model
    ).dicts()


def get_model_by_title(title: str):
    return models.Models.get(models.Models.title == title)