import models

if __name__ == '__main__':
    models.GeoKecamatan.drop_table()
    models.GeoKabupaten.drop_table()
    models.GeoProvinsi.drop_table()
