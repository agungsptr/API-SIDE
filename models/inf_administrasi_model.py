from .model import *


class InfAdministrasi(BaseModel):
    alamat = TextField(null=True)
    telp = CharField(null=True, max_length=15)
    email = CharField(null=True)
