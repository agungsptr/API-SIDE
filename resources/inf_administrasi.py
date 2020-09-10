from flask import Blueprint
from flask_restful import Resource, Api, reqparse, fields, marshal

from .resource import *

adm_fields = {
    'id': fields.Integer,
    'alamat': fields.String,
    'telp': fields.String,
    'email': fields.String
}


def get_or_abort(id):
    try:
        query = models.InfAdministrasi.get_by_id(id)
    except models.InfAdministrasi.DoesNotExist:
        abort(404)
    else:
        return query


class BaseAdm(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        super().__init__()

    def reqargs(self):
        self.reqparse.add_argument(
            'alamat',
            required=False, location=['form', 'json'])
        self.reqparse.add_argument(
            'telp', type=int,
            required=False, location=['form', 'json'])
        self.reqparse.add_argument(
            'email', type=email,
            required=False, location=['form', 'json'])


class GetPost(BaseAdm):
    # index
    @login_required
    def get(self):
        adm = [marshal(adm, adm_fields)
               for adm in models.InfAdministrasi.select()]
        return {'success': True,
                'data': adm}

    # store
    @login_required
    def post(self):
        self.reqargs()

        args = self.reqparse.parse_args()

        try:
            adm = models.InfAdministrasi.create(**args)
            return {'success': True,
                    'data': marshal(adm, adm_fields)}
        except models.InfAdministrasi.DoesNotExist:
            return {'success': False,
                    'message': 'Model does not exist'}


class GetPutDel(BaseAdm):
    # show
    @login_required
    def get(self, id):
        adm = get_or_abort(id)
        return {'success': True,
                'data': marshal(adm, adm_fields)}

    # edit
    @login_required
    def put(self, id):
        self.reqargs()

        get_or_abort(id)
        args = self.reqparse.parse_args()

        try:
            models.InfAdministrasi.update(**args).where(models.InfAdministrasi.id == id).execute()
            return {'success': True,
                    'data': marshal(get_or_abort(id), adm_fields)}
        except models.InfAdministrasi.DoesNotExist:
            return {'success': False,
                    'message': 'Model does not exist'}

    # delete
    @login_required
    def delete(self, id):
        get_or_abort(id)
        models.InfAdministrasi.delete().where(models.InfAdministrasi.id == id).execute()
        return {'success': True,
                'message': "Info Administrasi Desa is deleted"}


inf_administrasi_api = Blueprint('resources.inf_administrasi', __name__)
api = Api(inf_administrasi_api)
api.add_resource(GetPost, '/inf-administrasi', endpoint='inf-administrasi/gp')
api.add_resource(GetPutDel, '/inf-administrasi/<int:id>', endpoint='inf-administrasi/gpd')
