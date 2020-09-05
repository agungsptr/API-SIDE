from .model import *


class User(BaseModel):
    id = BigAutoField()
    name = CharField()
    username = CharField(unique=True)
    password = CharField()
    telp = CharField(max_length=15)
    alamat = TextField()
    jabatan = CharField(null=True)
    role = CharField()
