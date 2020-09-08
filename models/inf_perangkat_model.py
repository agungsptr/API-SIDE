from .model import *


class InfPerangkat(BaseModel):
    kades = CharField(null=True)
    sekdes = CharField(null=True)
    ku_tata_usaha = CharField(null=True)
    ku_keuangan = CharField(null=True)
    ku_perencanaan = CharField(null=True)
    ks_pemerintahan = CharField(null=True)
    ks_kesejahteraan = CharField(null=True)
    ks_pelayanan = CharField(null=True)
