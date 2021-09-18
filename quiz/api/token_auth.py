from flask_httpauth import HTTPTokenAuth

from quiz.api.errors import error_response
from quiz.models import User

token_auth = HTTPTokenAuth()


@token_auth.verify_token
def verify_token(token):
    if token:
        return User.check_token(token)
    else:
        return None


@token_auth.error_handler
def token_auth_error(status):
    return error_response(status)