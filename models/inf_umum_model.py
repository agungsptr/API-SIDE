from .model import *


class InfUmum(BaseModel):
    luas_desa = FloatField(null=True)
    total_dusun = IntegerField(null=True)
    bw_utara = CharField(null=True)
    bw_selatan = CharField(null=True)
    bw_timur = CharField(null=True)
    bw_barat = CharField(null=True)
    jp_kecamatan = FloatField(null=True)
    jp_kabupaten = FloatField(null=True)
    jp_provinsi = FloatField(null=True)
    link_maps = TextField(null=True)
