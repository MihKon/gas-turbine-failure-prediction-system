from database import models
# from database.models import database as db


def get_equipment():
    return models.Equipment.select().order_by(
        models.Equipment.id_equipment.desc()
    )


def get_parameters():
    return models.Parameters.select().order_by(
        models.Parameters.id_parameter.desc()
    )


def get_parameter_by_title(param_name: str):
    return models.Parameters.get(models.Parameters.par_name == param_name)
