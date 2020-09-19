import models


def drop_provinsi():
    models.GeoProvinsi.drop_table()


def drop_kabupaten():
    models.GeoKabupaten.drop_table()
