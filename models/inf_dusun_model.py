from .model import *


class InfDusun(BaseModel):
    id = AutoField()
    nama = CharField()
    kadus = CharField()
