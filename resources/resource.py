from flask import abort
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from functools import wraps


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user = get_jwt_identity()
        if user['role'] != 'ADMIN':
            return abort(403)
        else:
            return fn(*args, **kwargs)

    return wrapper
