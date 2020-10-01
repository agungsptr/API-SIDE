import inspect
import os
import sys

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from models import *


def drop():
    db.connect()
    db.drop_tables([User,
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
                    GeoKabupaten])
    db.close()


if __name__ == '__main__':
    drop()
