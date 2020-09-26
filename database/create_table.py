import models


def create_provinsi():
    models.db.connect()
    models.db.create_tables([models.GeoProvinsi], safe=True)
    models.db.close()


def create_kabupaten():
    models.db.connect()
    models.db.create_tables([models.GeoKabupaten], safe=True)
    models.db.close()


def create_penduduk():
    models.db.close()
    models.db.create_tables([models.Penduduk], safe=True)
    models.db.close()
