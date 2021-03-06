import os

from peewee import *

from config import *

env = os.environ.get("FLASK_ENV")

if env == "production":
    db = PostgresqlDatabase(
        database=Production.DB_NAME,
        user=Production.DB_USERNAME,
        host=Production.DB_HOST,
        port=Production.DB_PORT,
        password=Production.DB_PASSWORD)
else:
    db = MySQLDatabase(
        database=Development.DB_NAME,
        user=Development.DB_USERNAME,
        host=Development.DB_HOST,
        port=Development.DB_PORT,
        password=Development.DB_PASSWORD)


class BaseModel(Model):
    class Meta:
        database = db
