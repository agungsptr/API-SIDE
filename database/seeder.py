import inspect
import os
import sys

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from seeders import *


def seed():
    user_seeder()
    prov_seeder_all()
    kab_seeder_all()


if __name__ == '__main__':
    seed()
