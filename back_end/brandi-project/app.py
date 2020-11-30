from datetime import datetime

from flask import Flask
from flask.json import JSONEncoder
from flask_cors import CORS

from model import UserDao
from service import UserService
from view import user_endpoints


class CustomJsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        return super(JSONEncoder, self).default(obj)


def create_app():
    app = Flask(__name__)
    app.json_encoder = CustomJsonEncoder
    CORS(app, resources={r'*': {'origins': '*'}})

    # daos
    user_dao = UserDao()

    # service
    user_service = UserService(user_dao)

    # create endpoint
    app.register_blueprint(user_endpoints(user_service))

    return app
