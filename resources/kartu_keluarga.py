from flask import Blueprint
from flask_restful import Resource, reqparse, fields, marshal

from .resource import *

kk_fields = {
    'id': fields.String,
    'kepala_keluarga': fields.String,
    'provinsi': fields.String,
    'kabupaten': fields.String,
    'kecamatan': fields.String,
    'kelurahan': fields.String,
    'rt': fields.Integer,
    'rw': fields.Integer,
    'alamat': fields.String,
    'kode_pos': fields.String
}

penduduk_fields = {
    'id': fields.String,
    'nama': fields.String,
    'tempat_lahir': fields.String,
    'tanggal_lahir': fields.String,
    'jenis_kelamin': fields.String,
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
            'rt', type=int,
            required=False, help='Rt is required', location=['form', 'json'])
        self.reqparse.add_argument(
            'rw', type=int,
            required=False, help='Rw is required', location=['form', 'json'])
        self.reqparse.add_argument(
            'kode_pos',
            required=True, help='Kode Pos is required', location=['form', 'json'])


class GetPost(BaseKk):
    # index
    # @login_required
    def get(self):
        kk = [marshal(kk, kk_fields)
              for kk in models.KartuKeluarga.select()]
        return {'success': True,
                'data': kk}

    # store
    # @login_required
    def post(self):
        self.reqargs()

        args = self.reqparse.parse_args()

        try:
            models.KartuKeluarga.select().where(models.KartuKeluarga.id == args.get('id')).get()
        except models.KartuKeluarga.DoesNotExist:
            kk = models.KartuKeluarga.create(**args)
            return {'success': True,
                    'data': marshal(kk, kk_fields)}
        else:
            return {'success': False,
                    'message': 'Kartu Keluarga is registered'}


class GetPutDel(BaseKk):
    # show
    # @login_required
    def get(self, id):
        kk = get_or_abort(id)
        return {'success': True,
                'data': marshal(kk, kk_fields)}

    # edit
    # @login_required
    def put(self, id):
        self.reqargs()

        kk = get_or_abort(id)
        args = self.reqparse.parse_args()

        try:
            if kk.id != id:
                models.KartuKeluarga.select().where(models.KartuKeluarga.id == id).get()
            else:
                raise models.KartuKeluarga.DoesNotExist
        except models.KartuKeluarga.DoesNotExist:
            models.KartuKeluarga.update(**args).where(models.KartuKeluarga.id == id).execute()
            return {'success': True,
                    'data': marshal(get_or_abort(args.get('id')), kk_fields)}
        else:
            return {'success': False,
                    'message': 'Nomor KK alredy exist'}

    # delete
    # @login_required
    def delete(self, id):
        kk = get_or_abort(id)
        models.KartuKeluarga.delete().where(models.KartuKeluarga.id == id).execute()
        return {'success': True,
                'message': "Kartu Keluarga {} is deleted".format(kk.id)}


class GetPenduduk(BaseKk):
    # index
    # @login_required
    def get(self, id):
        kk = get_or_abort(id)
        kk_members = [marshal(member, penduduk_fields)
                      for member in kk.penduduk]
        return kk_members


kartu_keluarga_api = Blueprint('resources.kartu_keluarga', __name__)
api = Api(kartu_keluarga_api)
api.add_resource(GetPost, '/kartu-keluarga', endpoint='kartu-keluarga/gp')
api.add_resource(GetPutDel, '/kartu-keluarga/<string:id>', endpoint='kartu-keluarga/gpd')
api.add_resource(GetPenduduk, '/kartu-keluarga/member/<string:id>', endpoint='kartu-keluarga/member')
