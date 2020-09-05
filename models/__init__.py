from .model import *
from .user_model import User
from .kartu_keluarga_model import KartuKeluarga
from .penduduk_model import Penduduk
from .prog_desa_model import ProgDesa
from .inf_penduduk_model import InfPenduduk
from .inf_sarana_model import InfSarana
from .inf_perangkat_model import InfPerangkat
from .inf_umum_model import InfUmum
from .inf_administrasi_model import InfAdministrasi
from .inf_unggulan_model import InfUnggulan
from .inf_dusun_model import InfDusun


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
        InfDusun
    ], safe=True)
    db.close()
