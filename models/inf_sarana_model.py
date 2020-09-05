from .model import *


class InfSarana(BaseModel):
    id = AutoField()
    nama = CharField()
    alamat = TextField()
