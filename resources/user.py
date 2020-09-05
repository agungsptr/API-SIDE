from flask import Blueprint
from flask_jwt_extended import create_access_token
from flask_restful import Resource, Api, reqparse, fields, marshal
from werkzeug.security import generate_password_hash, check_password_hash

import models
from .resource import *

user_fields = {
    'name': fields.String,
    'username': fields.String,
    'telp': fields.String,
    'alamat': fields.String,
    'jabatan': fields.String,
    'role': fields.String
}


def get_or_abort(id):
    try:
        query = models.User.get_by_id(id)
    except models.User.DoesNotExist:
        abort(404)
    else:
        return query


class BaseUser(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        super().__init__()

    def reqvar(self):
        self.reqparse.add_argument(
            'name',
            required=True, help='Name is required', location=['form', 'json'])
        self.reqparse.add_argument(
            'username',
            required=True, help='Username is required', location=['form', 'json'])
        self.reqparse.add_argument(
            'password',
            required=True, help='Password is required', location=['form', 'json'])
        self.reqparse.add_argument(
            'telp',
            required=False, help='', location=['form', 'json'])
        self.reqparse.add_argument(
            'alamat',
            required=True, help='Alamat is required', location=['form', 'json'])
        self.reqparse.add_argument(
            'jabatan',
            required=False, help='', location=['form', 'json'])
        self.reqparse.add_argument(
            'role',
            required=True, help='Role is required', location=['form', 'json'])


class GetPost(BaseUser):
    # index
    @admin_required
    def get(self):
        # admin_required()
        return [marshal(user, user_fields)
                for user in models.User.select()]

    # store
    @admin_required
    def post(self):
        self.reqvar()

        args = self.reqparse.parse_args()
        username = args.get('username')

        try:
            models.User.select().where(models.User.username == username).get()
        except models.User.DoesNotExist:
            user = models.User.create(
                name=args.get('name'),
                username=username,
                password=generate_password_hash(args.get('password')),
                telp=args.get('telp'),
                alamat=args.get('alamat'),
                jabatan=args.get('jabatan'),
                role=args.get('role'))
            return {'success': True,
                    'message': marshal(user, user_fields)}
        else:
            return {'message': 'User is registered'}


class GetPutDel(BaseUser):
    # show
    @admin_required
    def get(self, id):
        user = get_or_abort(id)
        return marshal(user, user_fields)

    # edit
    @admin_required
    def put(self, id):
        self.reqvar()

        user = get_or_abort(id)
        args = self.reqparse.parse_args()
        user.update(
            name=args.get('name'),
            username=args.get('username'),
            password=generate_password_hash(args.get('password')),
            telp=args.get('telp'),
            alamat=args.get('alamat'),
            jabatan=args.get('jabatan'),
            role=args.get('role')).execute()
        return {'success': True,
                'message': marshal(get_or_abort(id), user_fields)}

    # delete
    @admin_required
    def delete(self, id):
        user = get_or_abort(id)
        user.delete().execute()
        return {'success': True,
                'message': "User {} is deleted".format(user.name)}


class Login(BaseUser):
    def post(self):
        self.reqparse.add_argument(
            'username',
            required=True, help='Username is required', location=['form', 'json'])
        self.reqparse.add_argument(
            'password',
            required=True, help='Password is required', location=['form', 'json'])

        args = self.reqparse.parse_args()
        username = args.get('username')
        password = args.get('password')

        try:
            user = models.User.get(models.User.username == username)

            if check_password_hash(user.password, password):
                identity = {'username': username,
                            'role': user.role}
                access_token = create_access_token(identity=identity)
                return {'success': True,
                        'message': marshal(user, user_fields),
                        'access_token': access_token}
            else:
                return {'message': 'User or Password is wrong'}
        except models.User.DoesNotExist:
            return {'message': 'User or Password is wrong'}


user_api = Blueprint('resources.user', __name__)
api = Api(user_api)
api.add_resource(GetPost, '/user', endpoint='user/gp')
api.add_resource(GetPutDel, '/user/<int:id>', endpoint='user/gpd')
api.add_resource(Login, '/user/login', endpoint='user/login')
