from .geo_kabupaten_model import GeoKabupaten
# from .geo_kecamatan_model import GeoKecamatan
from .geo_provinsi_model import GeoProvinsi
from .inf_administrasi_model import InfAdministrasi
from .inf_dusun_model import InfDusun
from .inf_penduduk_model import InfPenduduk
from .inf_perangkat_model import InfPerangkat
from .inf_sarana_model import InfSarana
from .inf_umum_model import InfUmum
from .inf_unggulan_model import InfUnggulan
from .kartu_keluarga_model import KartuKeluarga
from .model import *
from .penduduk_model import Penduduk
from .prog_desa_model import ProgDesa
from .user_model import User


def init():
    db.connect()
    db.create_tables([
        User,
        KartuKeluarga,
        Penduduk,
        ProgDesa,
        InfPenduduk,
        InfSarana,
        InfPerangkat,
        InfUmum,
        InfAdministrasi,
        InfUnggulan,
        InfDusun,
        GeoProvinsi,
        GeoKabupaten
        # GeoKecamatan
    ], safe=True)
    db.close()
