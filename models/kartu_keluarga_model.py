from .model import *


class KartuKeluarga(BaseModel):
    id = FixedCharField(primary_key=True, max_length=17)  # nomor kartu keluarga
    kepala_keluarga = CharField()
    provinsi = CharField()
    kabupaten = CharField()
    kecamatan = CharField()
    kelurahan = CharField()
    rt = IntegerField()
    rw = IntegerField()
    alamat = TextField()
    kode_pos = CharField(max_length=10)
