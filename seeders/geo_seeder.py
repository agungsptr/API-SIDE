import csv

import models


def prov_seeder(id, nama):
    try:
        prov = models.GeoProvinsi.create(id=id,
                                         nama=nama)
        print({'success': True,
               'prov': prov.nama})
    except models.GeoProvinsi.DoesNotExist:
        print({'success': False,
               'message': 'Model does not exist'})


def kab_seeder(id, nama, prov_id):
    try:
        kab = models.GeoKabupaten.create(id=id,
                                         nama=nama,
                                         geoprovinsi_id=prov_id)
        print({'success': True,
               'kab': kab.nama})
    except models.GeoKabupaten.DoesNotExist:
        print({'success': False,
               'message': 'Model does not exist'})


def kec_seeder(id, nama, kab_id):
    try:
        kec = models.GeoKecamatan.create(id=id,
                                         nama=nama,
                                         geokabupaten_id=kab_id)
        print({'success': True,
               'kab': kec.nama})
    except models.GeoKecamatan.DoesNotExist:
        print({'success': False,
               'message': 'Model does not exist'})


def get_prov_data():
    list_prov = []
    with open('./data/provinsi.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for i, row in enumerate(csv_reader):
            prov = []
            if i > 0:
                prov.append(row[0])
                prov.append(row[1])
                list_prov.append(prov)
    return list_prov


def get_kab_data():
    list_kab = []
    with open('./data/kabupaten.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for i, row in enumerate(csv_reader):
            kab = []
            if i > 0:
                kab.append(row[0])
                kab.append(row[1])
                kab.append(row[2])
                list_kab.append(kab)
    return list_kab


def get_kec_data():
    list_kec = []
    with open('./data/kecamatan.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for i, row in enumerate(csv_reader):
            kec = []
            if i > 0:
                kec.append(row[0])
                kec.append(row[1])
                kec.append(row[2])
                list_kec.append(kec)
    return list_kec


def prov_seeder_all():
    for prov in get_prov_data():
        prov_seeder(prov[0], prov[1])


def kab_seeder_all():
    for kab in get_kab_data():
        kab_seeder(kab[0], kab[1], kab[2])


def kec_seeder_all():
    for kec in get_kec_data():
        kec_seeder(kec[0], kec[1], kec[2])


if __name__ == '__main__':
    prov_seeder_all()
    kab_seeder_all()
    kec_seeder_all()