from flask import abort
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request, exceptions
from functools import wraps
from email_validator import validate_email, EmailNotValidError

import models


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except exceptions.NoAuthorizationError:
            return abort(403)

        identity = get_jwt_identity()
        try:
            user = models.User.select().where(models.User.username == identity).get()
            if user.role != 'ADMIN':
                return abort(403)
            else:
                return fn(*args, **kwargs)
        except models.User.DoesNotExist:
            return abort(403)

    return wrapper


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            return fn(*args, **kwargs)
        except exceptions.NoAuthorizationError:
            return abort(403)

    return wrapper


def email(email_str):
    try:
        valid = validate_email(email_str)
        return valid.email
    except EmailNotValidError:
        return abort(400)
