from .geo_provinsi_model import GeoProvinsi
from .model import *


class GeoKabupaten(BaseModel):
    id = AutoField()
    nama = CharField()
    provinsi_id = ForeignKeyField(GeoProvinsi, backref='kabupaten')
