from peewee import *

db = MySQLDatabase(
    database='side',
    user='root',
    host='127.0.0.1',
    port=3306)


class BaseModel(Model):
    class Meta:
        database = db
