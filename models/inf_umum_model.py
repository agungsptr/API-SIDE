from .model import *


class InfUmum(BaseModel):
    luas_desa = IntegerField()
    total_dusun = IntegerField()
    bw_utara = CharField()
    bw_selatan = CharField()
    bw_timur = CharField()
    bw_barat = CharField()
    jp_kecamatan = IntegerField()
    jp_kabupaten = IntegerField()
    jp_provinsi = IntegerField()
