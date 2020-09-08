from .model import *


class InfPenduduk(BaseModel):
    total_pria = IntegerField(null=True)
    total_wanita = IntegerField(null=True)
    total_kk = IntegerField(null=True)
    total_rtm = IntegerField(null=True)
