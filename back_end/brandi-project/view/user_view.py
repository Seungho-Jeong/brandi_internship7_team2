from flask import jsonify, Blueprint, request

from util.exception import ExistsException, NotExistsException
from db_connection  import db_connection
from service        import UserService
from model          import UserDao


class UserView:
    user_app = Blueprint('user_app', __name__, url_prefix='/user')

    def __init__(self, user_service):
        self.user_service = user_service

    @user_app.route('/signup', methods=['POST'])
    def sign_up():
        db = None
        try:
            data = request.json
            db = db_connection()

            UserService.sign_up(db, data)
            db.commit()

            return jsonify({'message' : 'SUCCESS'}), 200
        except KeyError as e:
            db.rollback()
            return jsonify({'message' : 'KEY_ERROR {}'.format(e)}), 400
        except ExistsException as e:
            return jsonify({'message' : 'ERROR {}'.format(e)}), 409
        except Exception as e:
            db.rollback()
            return jsonify({'message' : 'ERROR {}'.format(e)}), 500
        finally:
            if db:
                db.close()

    @user_app.route('/signin', methods=['POST'])
    def sign_in(self):
        db = None
        try:
            data = request.json
            db = db_connection()

            access_token = UserService.sign_in(db, data)

            return jsonify({'message' : 'SUCCESS', 'access_token' : access_token}), 200
        except NotExistsException as e:
            return jsonify({'message' : 'ERROR {}'.format(e)}), 400
        except Exception as e:
            return jsonify({'message' : 'ERROR {}'.format(e)}), 500
        finally:
            if db:
                db.close()

    @staticmethod
    @user_app.route('/category', methods=['GET'])
    def seller_category_type():
        db = None
        try:
            db = db_connection()

            result = UserService.seller_category_type(UserService(UserDao()), db)

            return jsonify({'message' : 'SUCCESS', 'category_list' : result}), 200
        except Exception as e:
            return jsonify({'message' : 'ERROR {}'.format(e)}), 500
        finally:
            if db:
                db.close()
