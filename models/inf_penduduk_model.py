from .model import *


class InfPenduduk(BaseModel):
    total_pria = IntegerField()
    total_wanita = IntegerField()
    total_kk = IntegerField()
    total_rtm = IntegerField()
