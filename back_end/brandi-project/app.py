from flask import Flask

from view    import UserView


def create_app():
    app = Flask(__name__)

    # view
    user_view = UserView()
    app.register_blueprint(user_view.user_app)

    return app
