from functools import wraps

from email_validator import validate_email, EmailNotValidError
from flask import abort, jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request, exceptions
from flask_restful import Api as _Api

import models


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except exceptions.NoAuthorizationError:
            return abort(403, "You don't have permission to access / on this server.")

        identity = get_jwt_identity()
        try:
            user = models.User.select().where(models.User.username == identity).get()
            if user.role != 'ADMIN':
                return abort(403)
            else:
                return fn(*args, **kwargs)
        except models.User.DoesNotExist:
            return abort(403, "You don't have permission to access / on this server.")

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


# Custome error handling
CUSTOM_ERRORS = {
    'ExpiredSignatureError': {'message': "Token has expired"},
}


class Api(_Api):
    def error_router(self, original_handler, e):
        """
        Override original error_router to only custom errors and parsing error (from webargs)
        if error can be handled by flask_restful's Api object, do so otherwise, let Flask handle the error
        the 'UnprocessableEntity' is included only because I'm also using webargs feel free to omit it

        :param original_handler:
        :param e:
        :return:
        """
        error_type = type(e).__name__.split(".")[-1]  # extract the error class name as a string
        if error_type in list(CUSTOM_ERRORS) + ['UnprocessableEntity']:
            return CUSTOM_ERRORS[str(error_type)]

        return jsonify(error=(str(e)))
