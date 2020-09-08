from flask import Blueprint
from flask_jwt_extended import jwt_required
from flask_restful import Resource, Api, reqparse, fields, marshal

from .resource import *

unggulan_fields = {
    'id': fields.String,
    'nama': fields.String
}


def get_or_abort(id):
    try:
        query = models.InfUnggulan.get_by_id(id)
    except models.InfUnggulan.DoesNotExist:
        abort(404)
    else:
        return query


class BaseUnggulan(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        super().__init__()

    def reqargs(self):
        self.reqparse.add_argument(
            'nama',
            required=True, help='Program Unggulan is required', location=['form', 'json'])


class GetPost(BaseUnggulan):
    # index
    @jwt_required
    def get(self):
        unggulan = [marshal(unggulan, unggulan_fields)
                    for unggulan in models.InfUnggulan.select()]
        return {'success': True,
                'data': unggulan}

    # store
    @jwt_required
    def post(self):
        self.reqargs()

        args = self.reqparse.parse_args()

        try:
            unggulan = models.InfUnggulan.create(**args)
            return {'success': True,
                    'data': marshal(unggulan, unggulan_fields)}
        except models.InfUnggulan.DoesNotExist:
            return {'success': False,
                    'message': 'Model does not exist'}


class GetPutDel(BaseUnggulan):
    # show
    @jwt_required
    def get(self, id):
        unggulan = get_or_abort(id)
        return {'success': True,
                'data': marshal(unggulan, unggulan_fields)}

    # edit
    @jwt_required
    def put(self, id):
        self.reqargs()

        get_or_abort(id)
        args = self.reqparse.parse_args()

        try:
            models.InfUnggulan.update(**args).where(models.InfUnggulan.id == id).execute()
            return {'success': True,
                    'data': marshal(get_or_abort(id), unggulan_fields)}
        except models.InfUnggulan.DoesNotExist:
            return {'success': False,
                    'message': 'Model does not exist'}

    # delete
    @jwt_required
    def delete(self, id):
        unggulan = get_or_abort(id)
        models.InfUnggulan.delete().where(models.InfUnggulan.id == id).execute()
        return {'success': True,
                'message': "Program Unggulan {} is deleted".format(unggulan.nama)}


inf_unggulan_api = Blueprint('resources.inf_unggulan', __name__)
api = Api(inf_unggulan_api)
api.add_resource(GetPost, '/inf-unggulan', endpoint='inf-unggulan/gp')
api.add_resource(GetPutDel, '/inf-unggulan/<int:id>', endpoint='inf-unggulan/gpd')
