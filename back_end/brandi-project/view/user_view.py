import jwt

from flask import jsonify, Blueprint, request

from util.exception import ExistsException, NotExistsException
from db_connection  import db_connection
from service        import UserService


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

            UserService.sign_up(UserService, db, data)
            db.commit()

            return jsonify({'message' : 'success'}), 200
        except ExistsException as e:
            db.rollback()
            return jsonify({'message' : e.message}), e.status_code
        except KeyError as e:
            db.rollback()
            return jsonify({'message' : 'key_error {}'.format(e)}), 400
        except Exception as e:
            db.rollback()
            return jsonify({'message' : 'error {}'.format(e)}), 500
        finally:
            if db:
                db.close()

    @user_app.route('/signin', methods=['POST'])
    def sign_in():
        db = None
        try:
            data = request.json
            db = db_connection()

            token = UserService.sign_in(UserService, db, data)
            db.commit()

            return jsonify({'message' : 'success', 'token' : token}), 200
        except NotExistsException as e:
            db.rollback()
            return jsonify({'message' : e.message}), e.status_code
        except KeyError as e:
            db.rollback()
            return jsonify({'message': 'error {}'.format(e)}), 400
        except Exception as e:
            db.rollback()
            return jsonify({'message' : 'error {}'.format(e)}), 500
        finally:
            if db:
                db.close()

    @user_app.route('/token', methods=['POST'])
    def reissuance_token():
        db = None
        try:
            data = request.json
            db = db_connection()

            token = UserService.reissuance_token(UserService, db, data)

            return jsonify({'message': 'success', 'access_token' : token}), 200
        except jwt.InvalidTokenError as e:
            return jsonify({'message': 'error {}'.format(e)}), 401
        except jwt.ExpiredSignatureError as e:
            return jsonify({'message': 'error {}'.format(e)}), 401
        except KeyError as e:
            return jsonify({'message': 'key_error {}'.format(e)}), 400
        except Exception as e:
            return jsonify({'message': 'error {}'.format(e)}), 500
        finally:
            if db:
                db.close()

    @user_app.route('/category', methods=['GET'])
    def seller_category_type():
        db = None
        try:
            db = db_connection()

            result = UserService.seller_category_type(UserService, db)

            return jsonify({'message' : 'success', 'category_list' : result}), 200
        except Exception as e:
            return jsonify({'message' : 'error {}'.format(e)}), 500
        finally:
            if db:
                db.close()
