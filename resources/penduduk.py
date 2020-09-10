from flask import Blueprint
from flask_restful import Resource, Api, reqparse, fields, marshal, inputs

from .resource import *

penduduk_fields = {
    'id': fields.String,
    'nama': fields.String,
    'tempat_lahir': fields.String,
    'tanggal_lahir': fields.String,
    'darah': fields.String,
    'alamat': fields.String,
    'kecamatan': fields.String,
    'kelurahan': fields.String,
    'rt': fields.Integer,
    'rw': fields.Integer,
    'agama': fields.String,
    'perkawinan': fields.String,
    'kewarganegaraan': fields.String,
    'status_hidup': fields.String,
    'kartukeluarga_id': fields.String
}


def get_or_abort(id, penduduk: bool):
    if penduduk:
        try:
            query = models.Penduduk.get_by_id(id)
        except models.Penduduk.DoesNotExist:
            abort(404)
        else:
            return query
    else:
        try:
            query = models.KartuKeluarga.get_by_id(id)
        except models.KartuKeluarga.DoesNotExist:
            abort(404, 'Nomor Kartu Keluarga not exist')
        else:
            return query


class BasePenduduk(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        super().__init__()

    def reqargs(self):
        self.reqparse.add_argument(
            'id',
            required=True, type=int, help='Nomor NIK is required', location=['form', 'json'])
        self.reqparse.add_argument(
            'nama',
            required=True, help='Nama is required', location=['form', 'json'])
        self.reqparse.add_argument(
            'tempat_lahir',
            required=True, help='Tempat Lahir is required', location=['form', 'json'])
        self.reqparse.add_argument(
            'tanggal_lahir', type=inputs.datetime_from_iso8601,
            required=True, help='Tanggal Lahir is required', location=['form', 'json'])
        self.reqparse.add_argument(
            'darah',
            required=False, location=['form', 'json'])
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
            'rt', type=int,
            required=False, help='Rt is required', location=['form', 'json'])
        self.reqparse.add_argument(
            'rw', type=int,
            required=False, help='Rw is required', location=['form', 'json'])
        self.reqparse.add_argument(
            'agama',
            required=True, help='Agama is required', location=['form', 'json'])
        self.reqparse.add_argument(
            'perkawinan',
            required=True, help='Status Perkawinan is required', location=['form', 'json'])
        self.reqparse.add_argument(
            'kewarganegaraan',
            required=True, help='Kewarganegaraan is required', location=['form', 'json'])
        self.reqparse.add_argument(
            'status_hidup',
            required=True, help='Status Hidup is required', location=['form', 'json'])
        self.reqparse.add_argument(
            'kartukeluarga_id',
            required=True, help='Nomor KK is required', location=['form', 'json'])


class GetPost(BasePenduduk):
    # index
    @login_required
    def get(self):
        penduduk = [marshal(penduduk, penduduk_fields)
                    for penduduk in models.Penduduk.select()]
        return {'success': True,
                'data': penduduk}

    # store
    # @login_required
    def post(self):
        self.reqargs()

        args = self.reqparse.parse_args()
        kk = args.get('kartukeluarga_id')
        get_or_abort(kk, False)

        try:
            models.Penduduk.select().where(models.Penduduk.id == args.get('id')).get()
        except models.Penduduk.DoesNotExist:
            penduduk = models.Penduduk.create(**args)
            return {'success': True,
                    'data': marshal(penduduk, penduduk_fields)}
        else:
            return {'success': False,
                    'message': 'Nomor NIK is alredy exist'}


class GetPutDel(BasePenduduk):
    # show
    @login_required
    def get(self, id):
        penduduk = get_or_abort(id, True)
        return {'success': True,
                'data': marshal(penduduk, penduduk_fields)}

    # edit
    @login_required
    def put(self, id):
        self.reqargs()

        penduduk = get_or_abort(id, True)
        args = self.reqparse.parse_args()

        kk = args.get('kartukeluarga_id')
        get_or_abort(kk, False)

        try:
            if penduduk.id != id:
                models.Penduduk.select().where(models.Penduduk.id == id).get()
            else:
                raise models.Penduduk.DoesNotExist
        except models.Penduduk.DoesNotExist:
            models.Penduduk.update(**args).where(models.Penduduk.id == id).execute()
            return {'success': True,
                    'data': marshal(get_or_abort(args.get('id'), True), penduduk_fields)}
        else:
            return {'success': False,
                    'message': 'Nomor NIK is alredy exist'}

    # delete
    @login_required
    def delete(self, id):
        penduduk = get_or_abort(id, True)
        models.Penduduk.delete().where(models.Penduduk.id == id).execute()
        return {'success': True,
                'message': "Kependudukan {} is deleted".format(penduduk.id)}


penduduk_api = Blueprint('resources.penduduk', __name__)
api = Api(penduduk_api)
api.add_resource(GetPost, '/penduduk', endpoint='penduduk/gp')
api.add_resource(GetPutDel, '/penduduk/<string:id>', endpoint='penduduk/gpd')
