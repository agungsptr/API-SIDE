from .geo_seeder import prov_seeder_all, kab_seeder_all, kec_seeder_all
from .user_seeder import user_seeder


def init():
    user_seeder()
    prov_seeder_all()
    kab_seeder_all()
