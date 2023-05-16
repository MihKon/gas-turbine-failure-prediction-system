from peewee import *

database = PostgresqlDatabase('diplomadbv2', **{'host': 'localhost', 'port': 5432, 'user': 'mihkon', 'password': 'postgres'})

class BaseModel(Model):
    class Meta:
        database = database

class Equipment(BaseModel):
    id_equipment = AutoField()
    equip_name = CharField()

    class Meta:
        table_name = 'equipment'

class Parameters(BaseModel):
    id_parameter = AutoField()
    par_name = CharField()

    class Meta:
        table_name = 'parameters'

class Measurings(BaseModel):
    id_measuring = IntegerField(constraints=[SQL("DEFAULT nextval('measurings_id_measuring_seq'::regclass)")])
    id_parameter = ForeignKeyField(column_name='id_parameter', field='id_parameter', model=Parameters)
    id_equipment = ForeignKeyField(column_name='id_equipment', field='id_equipment', model=Equipment)
    time_measuring = DateTimeField()
    value = FloatField()

    class Meta:
        table_name = 'measurings'
        indexes = (
            (('id_measuring', 'id_parameter'), True),
        )
        primary_key = CompositeKey('id_measuring', 'id_parameter')

class StandardParams(BaseModel):
    id_standard_parameter = AutoField()
    param_name = CharField()
    param_value = FloatField()

    class Meta:
        table_name = 'standard_params'

class Models(BaseModel):
    id_model = AutoField()
    title = CharField()
    path_to_file = TextField()
    id_standard_parameter = ForeignKeyField(column_name='id_standard_parameter', field='id_standard_parameter', model=StandardParams)

    class Meta:
        table_name = 'models'

class PredictParams(BaseModel):
    id_predict_param = AutoField()
    param_title = CharField()
    param_value = FloatField()
    id_model = ForeignKeyField(column_name='id_model', field='id_model', model=Models)

    class Meta:
        table_name = 'predict_params'

class Predicts(BaseModel):
    id_predict = AutoField()
    predict_time = DateTimeField()
    deviation = FloatField()
    verdict = IntegerField()
    id_measuring = ForeignKeyField(backref='measurings_id_measuring_set', column_name='id_measuring', field='id_parameter', model=Measurings)
    id_parameter = ForeignKeyField(backref='measurings_id_parameter_set', column_name='id_parameter', field='id_parameter', model=Measurings)
    id_model = ForeignKeyField(column_name='id_model', field='id_model', model=Models)

    class Meta:
        table_name = 'predicts'

