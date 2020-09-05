from .model import *


class InfPerangkat(BaseModel):
    kades = CharField()
    sekdes = CharField()
    ku_tata_usaha = CharField()
    ku_keuangan = CharField()
    ku_perencanaan = CharField()
    ks_pemerintahan = CharField()
    ks_kesejahteraan = CharField()
    ks_pelayanan = CharField()
