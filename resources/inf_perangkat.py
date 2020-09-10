from flask import Blueprint
from flask_restful import Resource, Api, reqparse, fields, marshal

from .resource import *

ip_fields = {
    'id': fields.Integer,
    'kades': fields.String,
    'sekdes': fields.Integer,
    'ku_tata_usaha': fields.String,
    'ku_keuangan': fields.String,
    'ku_perencanaan': fields.String,
    'ku_pemerintahan': fields.String,
    'ku_kesejahteraan': fields.String,
    'ku_pelayanan': fields.String
}


def get_or_abort(id):
    try:
        query = models.InfPerangkat.get_by_id(id)
    except models.InfPerangkat.DoesNotExist:
        abort(404)
    else:
        return query


class BaseIp(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        super().__init__()

    def reqargs(self):
        self.reqparse.add_argument(
            'kades',
            required=False, location=['form', 'json'])
        self.reqparse.add_argument(
            'sekdes',
            required=False, location=['form', 'json'])
        self.reqparse.add_argument(
            'ku_tata_usaha',
            required=False, location=['form', 'json'])
        self.reqparse.add_argument(
            'ku_keuangan',
            required=False, location=['form', 'json'])
        self.reqparse.add_argument(
            'ku_perencanaan',
            required=False, location=['form', 'json'])
        self.reqparse.add_argument(
            'ku_pemerintahan',
            required=False, location=['form', 'json'])
        self.reqparse.add_argument(
            'ku_kesejahteraan',
            required=False, location=['form', 'json'])
        self.reqparse.add_argument(
            'ku_pelayanan',
            required=False, location=['form', 'json'])


class GetPost(BaseIp):
    # index
    @login_required
    def get(self):
        ip = [marshal(ip, ip_fields)
              for ip in models.InfPerangkat.select()]
        return {'success': True,
                'data': ip}

    # store
    @login_required
    def post(self):
        self.reqargs()

        args = self.reqparse.parse_args()

        try:
            ip = models.InfPerangkat.create(**args)
            return {'success': True,
                    'data': marshal(ip, ip_fields)}
        except models.InfPerangkat.DoesNotExist:
            return {'success': False,
                    'message': 'Model does not exist'}


class GetPutDel(BaseIp):
    # show
    @login_required
    def get(self, id):
        ip = get_or_abort(id)
        return {'success': True,
                'data': marshal(ip, ip_fields)}

    # edit
    @login_required
    def put(self, id):
        self.reqargs()

        get_or_abort(id)
        args = self.reqparse.parse_args()

        try:
            models.InfPerangkat.update(**args).where(models.InfPerangkat.id == id).execute()
            return {'success': True,
                    'data': marshal(get_or_abort(id), ip_fields)}
        except models.InfPerangkat.DoesNotExist:
            return {'success': False,
                    'message': 'Model does not exist'}

    # delete
    @login_required
    def delete(self, id):
        get_or_abort(id)
        models.InfPerangkat.delete().where(models.InfPerangkat.id == id).execute()
        return {'success': True,
                'message': "Info Perangkat Desa is deleted"}


inf_perangkat_api = Blueprint('resources.inf_perangkat', __name__)
api = Api(inf_perangkat_api)
api.add_resource(GetPost, '/inf-perangkat', endpoint='inf-perangkat/gp')
api.add_resource(GetPutDel, '/inf-perangkat/<int:id>', endpoint='inf-perangkat/gpd')
