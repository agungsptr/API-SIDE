from .model import *


class InfAdministrasi(BaseModel):
    alamat = TextField()
    telp = CharField(max_length=15)
    email = CharField()
