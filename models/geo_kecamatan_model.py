from .geo_kabupaten_model import GeoKabupaten
from .model import *


class GeoKecamatan(BaseModel):
    id = AutoField()
    nama = CharField()
    geokabupaten_id = ForeignKeyField(GeoKabupaten, backref='kecamatan')
