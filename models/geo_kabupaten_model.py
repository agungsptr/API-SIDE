from models import *
from .geo_provinsi_model import GeoProvinsi


class GeoKabupaten(BaseModel):
    id = AutoField()
    nama = CharField()
    geoprovinsi_id = ForeignKeyField(GeoProvinsi, backref='kabupaten')
