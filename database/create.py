import inspect
import os
import sys

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from models import *


def create():
    db.connect()
    db.create_tables([User,
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
                      GeoKabupaten], safe=True)
    db.close()


if __name__ == '__main__':
    create()
