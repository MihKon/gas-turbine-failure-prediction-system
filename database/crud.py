import models
# from database.models import database as db


def get_equipment():
    return models.Equipment.select().order_by(
        models.Equipment.id_equipment
    ).dicts()


def get_parameters():
    return models.Parameters.select().order_by(
        models.Parameters.id_parameter
    ).dicts()


def get_parameter_by_title(param_name: str):
    return models.Parameters.get(models.Parameters.par_name == param_name)


def get_measurings(limit: int = None):
    return models.Measurings.select().limit(limit).order_by(
        models.Measurings.id_measuring.desc()
    ).dicts()


def create_measuring():
    pass