from flask import Blueprint
from flask_restful import Resource, Api, reqparse, fields, marshal

from .resource import *

dusun_fields = {
    'id': fields.Integer,
    'nama': fields.String,
    'kadus': fields.String
}


def get_or_abort(id):
    try:
        query = models.InfDusun.get_by_id(id)
    except models.InfDusun.DoesNotExist:
        abort(404)
    else:
        return query


class BaseDusun(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        super().__init__()

    def reqargs(self):
        self.reqparse.add_argument(
            'nama',
            required=True, help='Program Unggulan is required', location=['form', 'json'])
        self.reqparse.add_argument(
            'kadus',
            required=True, help='Kadus is required', location=['form', 'json'])


class GetPost(BaseDusun):
    # index
    @login_required
    def get(self):
        dusun = [marshal(dusun, dusun_fields)
                 for dusun in models.InfDusun.select()]
        return {'success': True,
                'data': dusun}

    # store
    @login_required
    def post(self):
        self.reqargs()

        args = self.reqparse.parse_args()

        try:
            dusun = models.InfDusun.create(**args)
            return {'success': True,
                    'data': marshal(dusun, dusun_fields)}
        except models.InfDusun.DoesNotExist:
            return {'success': False,
                    'message': 'Model does not exist'}


class GetPutDel(BaseDusun):
    # show
    @login_required
    def get(self, id):
        dusun = get_or_abort(id)
        return {'success': True,
                'data': marshal(dusun, dusun_fields)}

    # edit
    @login_required
    def put(self, id):
        self.reqargs()

        get_or_abort(id)
        args = self.reqparse.parse_args()

        try:
            models.InfDusun.update(**args).where(models.InfDusun.id == id).execute()
            return {'success': True,
                    'data': marshal(get_or_abort(id), dusun_fields)}
        except models.InfDusun.DoesNotExist:
            return {'success': False,
                    'message': 'Model does not exist'}

    # delete
    @login_required
    def delete(self, id):
        dusun = get_or_abort(id)
        models.InfDusun.delete().where(models.InfDusun.id == id).execute()
        return {'success': True,
                'message': "Dusun {} is deleted".format(dusun.nama)}


inf_dusun_api = Blueprint('resources.inf_dusun', __name__)
api = Api(inf_dusun_api)
api.add_resource(GetPost, '/inf-dusun', endpoint='inf-dusun/gp')
api.add_resource(GetPutDel, '/inf-dusun/<int:id>', endpoint='inf-dusun/gpd')
