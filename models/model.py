from peewee import *
from config import Config

db = PostgresqlDatabase(
    database=Config.DB_NAME,
    user=Config.DB_USERNAME,
    host=Config.DB_HOST,
    port=Config.DB_PORT)


class BaseModel(Model):
    class Meta:
        database = db
