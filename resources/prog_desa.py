from flask import Blueprint
from flask_jwt_extended import jwt_required
from flask_restful import Resource, Api, reqparse, fields, marshal

from .resource import *

pd_fields = {
    'id': fields.String,
    'program': fields.String
}


def get_or_abort(id):
    try:
        query = models.ProgDesa.get_by_id(id)
    except models.ProgDesa.DoesNotExist:
        abort(404)
    else:
        return query


class BasePd(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        super().__init__()

    def reqargs(self):
        self.reqparse.add_argument(
            'program',
            required=True, help='Program is required', location=['form', 'json'])


class GetPost(BasePd):
    # index
    @jwt_required
    def get(self):
        pd = [marshal(pd, pd_fields)
              for pd in models.ProgDesa.select()]
        return {'success': True,
                'data': pd}

    # store
    @jwt_required
    def post(self):
        self.reqargs()

        args = self.reqparse.parse_args()

        try:
            pd = models.ProgDesa.create(**args)
            return {'success': True,
                    'data': marshal(pd, pd_fields)}
        except models.ProgDesa.DoesNotExist:
            return {'success': False,
                    'message': 'Model does not exist'}


class GetPutDel(BasePd):
    # show
    @jwt_required
    def get(self, id):
        pd = get_or_abort(id)
        return {'success': True,
                'data': marshal(pd, pd_fields)}

    # edit
    @jwt_required
    def put(self, id):
        self.reqargs()

        get_or_abort(id)
        args = self.reqparse.parse_args()

        try:
            models.ProgDesa.update(**args).where(models.ProgDesa.id == id).execute()
            return {'success': True,
                    'data': marshal(get_or_abort(id), pd_fields)}
        except models.ProgDesa.DoesNotExist:
            return {'success': False,
                    'message': 'Model does not exist'}

    # delete
    @jwt_required
    def delete(self, id):
        pd = get_or_abort(id)
        models.ProgDesa.delete().where(models.ProgDesa.id == id).execute()
        return {'success': True,
                'message': "Program {} is deleted".format(pd.program)}


prog_desa_api = Blueprint('resources.prog_desa', __name__)
api = Api(prog_desa_api)
api.add_resource(GetPost, '/prog-desa', endpoint='prog-desa/gp')
api.add_resource(GetPutDel, '/prog-desa/<int:id>', endpoint='prog-desa/gpd')
