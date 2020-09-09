from peewee import *
from config import Production as pd

db = PostgresqlDatabase(
    database=pd.DB_NAME,
    user=pd.DB_USERNAME,
    host=pd.DB_HOST,
    port=pd.DB_PORT,
    password=pd.DB_PASSWORD)


class BaseModel(Model):
    class Meta:
        database = db
