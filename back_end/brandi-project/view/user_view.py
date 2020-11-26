import json

from flask import Blueprint, request

from util.exception import ExistsException, NotExistsException, JwtTokenException
from db_connection  import db_connection
from service        import UserService


class UserView:
    user_app = Blueprint('user_app', __name__, url_prefix='/user')

    def __init__(self, user_service):
        self.user_service = user_service

    @user_app.route('/signup', methods=['POST'])
    def sign_up(self):
        """
        유저 회원가입
        """

        db = None
        try:
            data = request.json
            db = db_connection()

            UserService.sign_up(UserService, db, data)
            db.commit()

            return json.dumps({'message' : 'success'}), 200
        except ExistsException as e:
            db.rollback()
            return json.dumps({'message' : e.message}), e.status_code
        except KeyError as e:
            db.rollback()
            return json.dumps({'message' : 'key_error'.format(e)}), 400
        except Exception as e:
            db.rollback()
            return json.dumps({'message' : 'error'.format(e)}), 500
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

            token = UserService.sign_in(UserService, db, data)
            db.commit()

            return json.dumps({'message' : 'success', 'token' : token}), 200
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

            token = UserService.reissuance_token(UserService, db, data)

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

            result = UserService.seller_category_type(UserService, db)

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

            data = {'sql' : ''}
            result = UserService.get_seller_information(UserService, db, data)

            return json.dumps({'message': 'success', 'seller_info': result}, ensure_ascii=False), 200
        except NotExistsException as e:
            return json.dumps({'message': e.message}), e.status_code
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

            data = {'seller_id' : seller_id}
            result = UserService.get_seller_information(UserService, db, data)
            # result = self.user_service.get_seller_information(db, data)

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
            UserService.update_seller_information(UserService, db, data)

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
            UserService.update_shop_status(UserService, db, data)

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

