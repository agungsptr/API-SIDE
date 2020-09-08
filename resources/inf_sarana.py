from flask import Blueprint
from flask_jwt_extended import jwt_required
from flask_restful import Resource, Api, reqparse, fields, marshal

from .resource import *

sarana_fields = {
    'id': fields.String,
    'nama': fields.String,
    'alamat': fields.String
}


def get_or_abort(id):
    try:
        query = models.InfSarana.get_by_id(id)
    except models.InfSarana.DoesNotExist:
        abort(404)
    else:
        return query


class BaseSarana(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        super().__init__()

    def reqargs(self):
        self.reqparse.add_argument(
            'nama',
            required=True, help='Program Unggulan is required', location=['form', 'json'])
        self.reqparse.add_argument(
            'alamat',
            required=True, help='Alamat is required', location=['form', 'json'])


class GetPost(BaseSarana):
    # index
    # @jwt_required
    def get(self):
        sarana = [marshal(sarana, sarana_fields)
                    for sarana in models.InfSarana.select()]
        return {'success': True,
                'data': sarana}

    # store
    # @jwt_required
    def post(self):
        self.reqargs()

        args = self.reqparse.parse_args()

        try:
            sarana = models.InfSarana.create(**args)
            return {'success': True,
                    'data': marshal(sarana, sarana_fields)}
        except models.InfSarana.DoesNotExist:
            return {'success': False,
                    'message': 'Model does not exist'}


class GetPutDel(BaseSarana):
    # show
    # @jwt_required
    def get(self, id):
        sarana = get_or_abort(id)
        return {'success': True,
                'data': marshal(sarana, sarana_fields)}

    # edit
    # @jwt_required
    def put(self, id):
        self.reqargs()

        get_or_abort(id)
        args = self.reqparse.parse_args()

        try:
            models.InfSarana.update(**args).where(models.InfSarana.id == id).execute()
            return {'success': True,
                    'data': marshal(get_or_abort(id), sarana_fields)}
        except models.InfSarana.DoesNotExist:
            return {'success': False,
                    'message': 'Model does not exist'}

    # delete
    # @jwt_required
    def delete(self, id):
        sarana = get_or_abort(id)
        models.InfSarana.delete().where(models.InfSarana.id == id).execute()
        return {'success': True,
                'message': "Sarana {} is deleted".format(sarana.nama)}


inf_sarana_api = Blueprint('resources.inf_sarana', __name__)
api = Api(inf_sarana_api)
api.add_resource(GetPost, '/inf-sarana', endpoint='inf-sarana/gp')
api.add_resource(GetPutDel, '/inf-sarana/<int:id>', endpoint='inf-sarana/gpd')
