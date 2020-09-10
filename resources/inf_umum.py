from flask import Blueprint
from flask_restful import Resource, Api, reqparse, fields, marshal

from .resource import *

umum_fields = {
    'id': fields.Integer,
    'luas_desa': fields.Float,
    'total_dusun': fields.Integer,
    'bw_utara': fields.String,
    'bw_selatan': fields.String,
    'bw_timur': fields.String,
    'bw_barat': fields.String,
    'jp_kecamatan': fields.Float,
    'jp_kabupaten': fields.Float,
    'jp_provinsi': fields.Float
}


def get_or_abort(id):
    try:
        query = models.InfUmum.get_by_id(id)
    except models.InfUmum.DoesNotExist:
        abort(404)
    else:
        return query


class BaseUmum(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        super().__init__()

    def reqargs(self):
        self.reqparse.add_argument(
            'luas_desa', type=float,
            required=False, location=['form', 'json'])
        self.reqparse.add_argument(
            'total_dusun', type=int,
            required=False, location=['form', 'json'])
        self.reqparse.add_argument(
            'bw_utara',
            required=False, location=['form', 'json'])
        self.reqparse.add_argument(
            'bw_selatan',
            required=False, location=['form', 'json'])
        self.reqparse.add_argument(
            'bw_timur',
            required=False, location=['form', 'json'])
        self.reqparse.add_argument(
            'bw_barat',
            required=False, location=['form', 'json'])
        self.reqparse.add_argument(
            'jp_kecamatan', type=float,
            required=False, location=['form', 'json'])
        self.reqparse.add_argument(
            'jp_kabupaten', type=float,
            required=False, location=['form', 'json'])
        self.reqparse.add_argument(
            'jp_provinsi', type=float,
            required=False, location=['form', 'json'])


class GetPost(BaseUmum):
    # index
    @login_required
    def get(self):
        umum = [marshal(umum, umum_fields)
                for umum in models.InfUmum.select()]
        return {'success': True,
                'data': umum}

    # store
    @login_required
    def post(self):
        self.reqargs()

        args = self.reqparse.parse_args()

        try:
            umum = models.InfUmum.create(**args)
            return {'success': True,
                    'data': marshal(umum, umum_fields)}
        except models.InfUmum.DoesNotExist:
            return {'success': False,
                    'message': 'Model does not exist'}


class GetPutDel(BaseUmum):
    # show
    @login_required
    def get(self, id):
        umum = get_or_abort(id)
        return {'success': True,
                'data': marshal(umum, umum_fields)}

    # edit
    @login_required
    def put(self, id):
        self.reqargs()

        get_or_abort(id)
        args = self.reqparse.parse_args()

        try:
            models.InfUmum.update(**args).where(models.InfUmum.id == id).execute()
            return {'success': True,
                    'data': marshal(get_or_abort(id), umum_fields)}
        except models.InfUmum.DoesNotExist:
            return {'success': False,
                    'message': 'Model does not exist'}

    # delete
    @login_required
    def delete(self, id):
        get_or_abort(id)
        models.InfUmum.delete().where(models.InfUmum.id == id).execute()
        return {'success': True,
                'message': "Info Umum Desa is deleted"}


inf_umum_api = Blueprint('resources.inf_umum', __name__)
api = Api(inf_umum_api)
api.add_resource(GetPost, '/inf-umum', endpoint='inf-umum/gp')
api.add_resource(GetPutDel, '/inf-umum/<int:id>', endpoint='inf-umum/gpd')
