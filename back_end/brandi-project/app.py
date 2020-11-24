from flask import Flask

from model   import UserDao
from service import UserService
from view    import UserView


def create_app():
    app = Flask(__name__)

    # dao
    user_dao = UserDao()

    # service
    user_service = UserService(user_dao)

    # view
    user_view = UserView(user_service)
    app.register_blueprint(user_view.user_app)

    return app
