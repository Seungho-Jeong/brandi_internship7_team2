from flask import Flask
from flask_cors import CORS

from model import UserDao
from service import UserService
from view import user_endpoints


def create_app():
    app = Flask(__name__)
    CORS(app, resources={r'*': {'origins': '*'}})

    # dao
    user_dao = UserDao()

    # service
    user_service = UserService(user_dao)

    # create endpoint
    app.register_blueprint(user_endpoints(user_service))

    return app
