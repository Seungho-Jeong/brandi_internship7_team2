import json

from flask import Blueprint, request

from util.exception import ExistsException, NotExistsException, JwtTokenException
from db_connection  import db_connection
from service        import UserService


class UserView:
    user_app = Blueprint('user_app', __name__, url_prefix='/user')

    @user_app.route('/signup', methods=['POST'])
    def sign_up(*args):
        """
        유저 회원가입
        """

        db = None
        try:
            data = request.json
            db = db_connection()

            user_service = UserService()
            user_service.sign_up(db, data)
            db.commit()

            return json.dumps({'message' : 'success'}), 200
        except ExistsException as e:
            db.rollback()
            return json.dumps({'message' : e.message}), e.status_code
        except KeyError as e:
            db.rollback()
            return json.dumps({'message' : 'key_error {}'.format(e)}), 400
        except Exception as e:
            db.rollback()
            return json.dumps({'message' : 'error {}'.format(e)}), 500
        finally:
            if db:
                db.close()

    @user_app.route('/signin', methods=['POST'])
    def sign_in():
        """
        유저 로그인
        :return: access_token, refresh_token
        """

        db = None
        try:
            data = request.json
            db = db_connection()

            user_service = UserService()
            access_token = user_service.sign_in(db, data)
            db.commit()

            return json.dumps({'message' : 'success', 'access_token' : access_token}), 200
        except NotExistsException as e:
            db.rollback()
            return json.dumps({'message' : e.message}), e.status_code
        except KeyError as e:
            db.rollback()
            return json.dumps({'message': 'error {}'.format(e)}), 400
        except Exception as e:
            db.rollback()
            return json.dumps({'message' : 'error {}'.format(e)}), 500
        finally:
            if db:
                db.close()

    @user_app.route('/token', methods=['POST'])
    def reissuance_token():
        """
        access_token 만료 시 재발급
        :return: access_token
        """

        db = None
        try:
            data = request.json
            db = db_connection()

            user_service = UserService()
            token = user_service.reissuance_token(db, data)

            return json.dumps({'message': 'success', 'access_token' : token}), 200
        except JwtTokenException as e:
            return json.dumps({'message': e.message}), e.status_code
        except KeyError as e:
            return json.dumps({'message': 'key_error {}'.format(e)}), 400
        except Exception as e:
            return json.dumps({'message': 'error {}'.format(e)}), 500
        finally:
            if db:
                db.close()

    @user_app.route('/category', methods=['GET'])
    def seller_category_type():
        """
        셀러 카테고리 정보 가져오기
        :return: 카테고리 리스트
        """

        db = None
        try:
            db = db_connection()

            user_service = UserService()
            result = user_service.seller_category_type(db)

            return json.dumps({'message' : 'success', 'category_list' : result}), 200
        except Exception as e:
            return json.dumps({'message' : 'error {}'.format(e)}), 500
        finally:
            if db:
                db.close()

    @user_app.route('', methods=['GET'])
    def get_seller_list():
        db = None
        try:
            db = db_connection()
            filters = dict(request.args)

            user_service = UserService()
            sellers = user_service.get_seller_list(db, filters)

            return json.dumps({'message': 'success', 'list_count' : sellers['count'],
                               'seller_list': sellers['seller_list']}, ensure_ascii=False), 200
        except Exception as e:
            return json.dumps({'message': 'error {}'.format(e)}), 500
        finally:
            if db:
                db.close()

    @user_app.route('/my_page/<int:seller_id>', methods=['GET'])
    def get_seller_information(seller_id):
        """
        셀러 상세정보 가져오기
        :return: 셀러 상세정보
        """

        db = None
        try:
            db = db_connection()

            user_service = UserService()
            result = user_service.get_seller_information(db, seller_id)

            return json.dumps({'message': 'success', 'seller_info': result}, ensure_ascii=False), 200
        except NotExistsException as e:
            return json.dumps({'message' : e.message}), e.status_code
        except Exception as e:
            return json.dumps({'message': 'error {}'.format(e)}), 500
        finally:
            if db:
                db.close()

    @user_app.route('/my_page/<int:seller_id>', methods=['PUT'])
    def update_seller_information(seller_id):
        db = None
        try:
            data = request.json
            db = db_connection()

            data['seller_id'] = seller_id
            user_service = UserService()
            user_service.update_seller_information(db, data)

            db.commit()

            return json.dumps({'message': 'success'}), 200
        except KeyError as e:
            db.rollback()
            return json.dumps({'message' : 'key_error {}'.format(e)}), 400
        except Exception as e:
            db.rollback()
            return json.dumps({'message': 'error {}'.format(e)}), 500
        finally:
            if db:
                db.close()

    @user_app.route('/my_page/<int:seller_id>', methods=['PATCH'])
    def update_shop_status(seller_id):
        db = None
        try:
            db = db_connection()

            data = {'seller_id' : seller_id}
            user_service = UserService()
            user_service.update_shop_status(db, data)

            db.commit()

            return json.dumps({'message': 'success'}), 200
        except KeyError as e:
            db.rollback()
            return json.dumps({'message': 'key_error {}'.format(e)}), 400
        except Exception as e:
            db.rollback()
            return json.dumps({'message': 'error {}'.format(e)}), 500
        finally:
            if db:
                db.close()

