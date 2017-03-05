import os
from base64 import standard_b64encode


def create_authentication_value(authentication_model):
    return {
        'token': _create_athentication_token
    }[authentication_model]()


def _create_athentication_token():
    return standard_b64encode(os.urandom(16))[:-2]
