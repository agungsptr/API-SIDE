from flask import Blueprint
from flask_jwt_extended import jwt_required
from flask_restful import Resource, Api, reqparse, fields, marshal

import models
from .resource import *

kk_fields = {
    'id': fields.String,
    'kepala_keluarga': fields.String,
    'provinsi': fields.String,
    'kabupaten': fields.String,
    'kecamatan': fields.String,
    'kelurahan': fields.String,
    'rt': fields.String,
    'rw': fields.String,
    'alamat': fields.String,
    'kode_pos': fields.Integer
}


def get_or_abort(id):
    try:
        query = models.KartuKeluarga.get_by_id(id)
    except models.KartuKeluarga.DoesNotExist:
        abort(404)
    else:
        return query


class BaseKk(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        super().__init__()

    def reqargs(self):
        self.reqparse.add_argument(
            'id',
            required=True, help='Nomor Kartu Keluarga is required', location=['form', 'json'])
        self.reqparse.add_argument(
            'kepala_keluarga',
            required=True, help='Nama Kepala Keluarga is required', location=['form', 'json'])
        self.reqparse.add_argument(
            'provinsi',
            required=True, help='Provinsi is required', location=['form', 'json'])
        self.reqparse.add_argument(
            'kabupaten',
            required=True, help='Kabupaten is required', location=['form', 'json'])
        self.reqparse.add_argument(
            'alamat',
            required=True, help='Alamat is required', location=['form', 'json'])
        self.reqparse.add_argument(
            'kecamatan',
            required=True, help='Kecamatan is required', location=['form', 'json'])
        self.reqparse.add_argument(
            'kelurahan',
            required=True, help='Kelurahan is required', location=['form', 'json'])
        self.reqparse.add_argument(
            'rt',
            required=False, help='Rt is required', location=['form', 'json'])
        self.reqparse.add_argument(
            'rw',
            required=False, help='Rw is required', location=['form', 'json'])
        self.reqparse.add_argument(
            'kode_pos',
            required=True, help='Kode Pos is required', location=['form', 'json'])


class GetPost(BaseKk):
    # index
    @jwt_required
    def get(self):
        return [marshal(kk, kk_fields)
                for kk in models.KartuKeluarga.select()]

    # store
    @jwt_required
    def post(self):
        self.reqargs()

        args = self.reqparse.parse_args()

        try:
            models.KartuKeluarga.select().where(models.KartuKeluarga.id == args.get('id')).get()
        except models.KartuKeluarga.DoesNotExist:
            kk = models.KartuKeluarga.create(**args)
            return {'success': True,
                    'message': marshal(kk, kk_fields)}
        else:
            return {'message': 'Kartu Keluarga is registered'}


class GetPutDel(BaseKk):
    # show
    @jwt_required
    def get(self, id):
        kk = get_or_abort(id)
        return marshal(kk, kk_fields)

    # edit
    @jwt_required
    def put(self, id):
        self.reqargs()

        kk = get_or_abort(id)
        args = self.reqparse.parse_args()
        kk.update(args).execute()
        return {'success': True,
                'message': marshal(get_or_abort(args.get('id')), kk_fields)}

    # delete
    @jwt_required
    def delete(self, id):
        user = get_or_abort(id)
        user.delete().execute()
        return {'success': True,
                'message': "User {} is deleted".format(user.name)}


kartu_keluarga_api = Blueprint('resources.kartu_keluarga', __name__)
api = Api(kartu_keluarga_api)
api.add_resource(GetPost, '/kartukeluarga', endpoint='kartukeluarga/gp')
api.add_resource(GetPutDel, '/kartukeluarga/<string:id>', endpoint='kartukeluarga/gpd')
