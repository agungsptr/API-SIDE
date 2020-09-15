from models import *
from .geo_kabupaten_model import GeoKabupaten


class GeoKecamatan(BaseModel):
    id = AutoField()
    nama = CharField()
    geokabupaten_id = ForeignKeyField(GeoKabupaten, backref='kecamatan')
