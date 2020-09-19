from flask import Blueprint
from flask_restful import fields, marshal, Resource

from .resource import *

prov_fields = {
    'id': fields.Integer,
    'nama': fields.String
}

kab_fields = {
    'id': fields.Integer,
    'nama': fields.String,
    'provinsi_id': fields.String
}


def get_or_abort(id, lvl: int):
    if lvl == 1:
        try:
            query = models.GeoProvinsi.get_by_id(id)
        except models.GeoProvinsi.DoesNotExist:
            abort(404)
        else:
            return query
    elif lvl == 2:
        try:
            query = models.GeoKabupaten.select().where(models.GeoKabupaten.provinsi_id == id).get()
        except models.GeoKabupaten.DoesNotExist:
            abort(404)
        else:
            return query
    else:
        return abort(404)


class GetProv(Resource):
    # @login_required
    def get(self):
        prov = [marshal(prov, prov_fields)
                for prov in models.GeoProvinsi.select()]
        return {'success': True,
                'data': prov}


class GetKab(Resource):
    # @login_required
    def get(self, id):
        get_or_abort(id, 2)

        kab = [marshal(kab, kab_fields)
               for kab in models.GeoKabupaten.select().where(models.GeoKabupaten.provinsi_id == id)]
        return {'success': True,
                'data': kab}


geo_api = Blueprint('resources.geo', __name__)
api = Api(geo_api)
api.add_resource(GetProv, '/geo/provinsi', endpoint='geo/provinsi')
api.add_resource(GetKab, '/geo/kabupaten/<int:id>', endpoint='geo/kabupaten')
