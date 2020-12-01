from datetime import datetime

from flask import Flask
from flask.json import JSONEncoder
from flask_cors import CORS

from model import UserDao, ProductDao
from service import UserService, ProductService
from view import user_endpoints, product_endpoints


class CustomJsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        return super(JSONEncoder, self).default(obj)


def create_app():
    app = Flask(__name__)
    CORS(app, resources={r'*': {'origins': '*'}})
    app.json_encoder = CustomJsonEncoder

    # dao
    user_dao = UserDao()
    product_dao = ProductDao()

    # service
    user_service = UserService(user_dao)
    product_service = ProductService(product_dao)

    # create endpoint
    app.register_blueprint(user_endpoints(user_service))
    app.register_blueprint(product_endpoints(product_service))

    return app
