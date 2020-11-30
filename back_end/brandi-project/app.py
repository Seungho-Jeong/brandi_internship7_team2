from flask import Flask, Blueprint
from flask_cors import CORS

from model import UserDao, ProductDao
from service import UserService, ProductService
from view import user_endpoints, product_endpoints


def create_app():
    app = Flask(__name__)
    CORS(app, resources={r'*': {'origins': '*'}})

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
