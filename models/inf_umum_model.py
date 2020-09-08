from .model import *


class InfUmum(BaseModel):
    luas_desa = IntegerField(null=True)
    total_dusun = IntegerField(null=True)
    bw_utara = CharField(null=True)
    bw_selatan = CharField(null=True)
    bw_timur = CharField(null=True)
    bw_barat = CharField(null=True)
    jp_kecamatan = IntegerField(null=True)
    jp_kabupaten = IntegerField(null=True)
    jp_provinsi = IntegerField(null=True)
