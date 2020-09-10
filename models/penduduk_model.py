from .kartu_keluarga_model import KartuKeluarga
from .model import *


class Penduduk(BaseModel):
    id = FixedCharField(primary_key=True, max_length=17)  # nomor ktp
    nama = CharField()
    tempat_lahir = CharField()
    tanggal_lahir = DateTimeField()
    darah = CharField(max_length=5, null=True)
    alamat = TextField()
    kecamatan = CharField()
    kelurahan = CharField()
    rt = IntegerField()
    rw = IntegerField()
    agama = CharField()
    perkawinan = CharField()
    kewarganegaraan = CharField()
    status_hidup = CharField()
    kartukeluarga_id = ForeignKeyField(KartuKeluarga, backref='penduduk')
