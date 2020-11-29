import json

from flask import Blueprint, request

from util.exception import ExistsException, NotExistsException, JwtTokenException
from db_connection  import db_connection
from util.decorator import login_decorator


def user_endpoints(user_service):
    user_app = Blueprint('user_app', __name__, url_prefix='/user')

    @user_app.route('/signup', methods=['POST'])
    def sign_up():
        """
        유저 회원가입
        """

        db = None
        try:
            data = request.json
            db = db_connection()

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

            access_token = user_service.sign_in(db, data)
            db.commit()

            return json.dumps({'message' : 'success', 'access_token' : access_token}), 200
        except NotExistsException as e:
            db.rollback()
            return json.dumps({'message' : e.message}), e.status_code
        except KeyError as e:
            db.rollback()
            return json.dumps({'message': 'key_error {}'.format(e)}), 400
        except Exception as e:
            db.rollback()
            return json.dumps({'message' : 'error {}'.format(e)}), 500
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

            result = user_service.seller_category_type(db)

            return json.dumps({'message' : 'success', 'category_list' : result}), 200
        except Exception as e:
            return json.dumps({'message' : 'error {}'.format(e)}), 500
        finally:
            if db:
                db.close()

    @user_app.route('', methods=['GET'])
    @login_decorator
    def get_seller_list():
        """
        셀러 회원목록 리스트 및 목록 개수
        :return: 회원목록 리스트 및 개수
        """

        db = None
        try:
            db = db_connection()
            filters = dict(request.args)

            sellers = user_service.get_seller_list(db, filters)

            return json.dumps({'message' : 'success', 'list_count' : sellers['count'],
                               'seller_list' : sellers['seller_list']}, ensure_ascii=False), 200
        except Exception as e:
            return json.dumps({'message': 'error {}'.format(e)}), 500
        finally:
            if db:
                db.close()

    @user_app.route('/<int:seller_id>', methods=['GET'])
    @login_decorator
    def get_seller_information(seller_id):
        """
        셀러 상세정보 가져오기
        :return: 셀러 상세정보
        """

        db = None
        try:
            db = db_connection()

            result = user_service.get_seller_information(db, seller_id)

            return json.dumps({'message' : 'success', 'seller_info': result}, ensure_ascii=False), 200
        except NotExistsException as e:
            return json.dumps({'message' : e.message}), e.status_code
        except Exception as e:
            return json.dumps({'message' : 'error {}'.format(e)}), 500
        finally:
            if db:
                db.close()

    @user_app.route('/<int:seller_id>', methods=['PUT'])
    @login_decorator
    def update_seller_information(seller_id):
        """
        셀러 상세정보 수정
        :param seller_id: seller_id
        """

        db = None
        try:
            data = request.json
            db = db_connection()

            user_service.update_seller_information(db, data, seller_id)

            db.commit()

            return json.dumps({'message' : 'success'}), 200
        except KeyError as e:
            db.rollback()
            return json.dumps({'message' : 'key_error {}'.format(e)}), 400
        except Exception as e:
            db.rollback()
            return json.dumps({'message' : 'error {}'.format(e)}), 500
        finally:
            if db:
                db.close()

    @user_app.route('/<int:seller_id>', methods=['PATCH'])
    @login_decorator
    def update_shop_status(seller_id):
        """
        셀러 상태(입점상태) 수정
        :param seller_id: seller_id
        """

        db = None
        try:
            data = request.json
            db = db_connection()

            user_service.update_shop_status(db, data, seller_id)

            db.commit()

            return json.dumps({'message' : 'success'}), 200
        except KeyError as e:
            db.rollback()
            return json.dumps({'message' : 'key_error {}'.format(e)}), 400
        except Exception as e:
            db.rollback()
            return json.dumps({'message' : 'error {}'.format(e)}), 500
        finally:
            if db:
                db.close()

    @user_app.route('/<int:seller_id>/manager', methods=['POST'])
    @login_decorator
    def create_manager(seller_id):
        """
        담당 매니저 생성
        :param seller_id: seller_id
        """

        db = None
        try:
            data = request.json
            db = db_connection()

            user_service.create_managers(db, data, seller_id)
            db.commit()
            return json.dumps({'message' : 'success'}), 200
        except KeyError as e:
            db.rollback()
            return json.dumps({'message' : 'key_error {}'.format(e)}), 400
        except Exception as e:
            db.rollback()
            return json.dumps({'message' : 'error {}'.format(e)}), 500

    return user_app
