from flask import Blueprint, request, jsonify

from util.exception import ExistsException, NotExistsException, InvalidValueException
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
        """
        유저 로그인
        :return: access_token
        """

        db = None
        try:
            data = request.json
            db = db_connection()

            access_token = user_service.sign_in(db, data)
            db.commit()

            return jsonify({'message' : 'success', 'access_token' : access_token}), 200
        except NotExistsException as e:
            db.rollback()
            return jsonify({'message' : e.message}), e.status_code
        except KeyError as e:
            db.rollback()
            return jsonify({'message': 'key_error {}'.format(e)}), 400
        except Exception as e:
            db.rollback()
            return jsonify({'message' : 'error {}'.format(e)}), 500
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

            category_list = user_service.seller_category_type(db)

            return jsonify({'message' : 'success', 'category_list' : category_list}), 200
        except Exception as e:
            return jsonify({'message' : 'error {}'.format(e)}), 500
        finally:
            if db:
                db.close()

    @user_app.route('', methods=['GET'])
    @login_decorator
    def get_seller_list():
        """
        셀러 회원목록 리스트 및 목록 개수
        마스터 토큰이 아닐 시 permission denied
        필터의 key 값이 잘못되었을 때 invalid input 'key' in filters
        end_date 가 start_date 보다 이전날짜로 입력되었을때는 예외처리
        :return: 회원목록 리스트 및 개수
        """

        db = None
        try:
            db = db_connection()

            if not request.is_master:
                return jsonify({'message' : 'permission denied'}), 403

            filter_list = ['id', 'account', 'name_en', 'name_ko',
                           'manager_name', 'manager_mobile', 'manager_email',
                           'category', 'start_date', 'end_date',
                           'offset', 'limit']

            filters = dict(request.args)

            for key in filters:
                if key not in filter_list:
                    return jsonify({'message' : 'invalid input {} in filters'.format(key)}), 400

            if ('start_date' in filters) and ('end_date' in filters):
                if filters['end_date'] < filters['start_date']:
                    raise InvalidValueException('end_date should not earlier than start_date', 400)

            sellers = user_service.get_seller_list(db, filters)

            return jsonify({'message' : 'success', 'total_count' : sellers['count'],
                            'seller_list' : sellers['seller_list']}), 200
        except InvalidValueException as e:
            return jsonify({'message' : e.message}), e.status_code
        except Exception as e:
            return jsonify({'message' : 'error {}'.format(e)}), 500
        finally:
            if db:
                db.close()

    @user_app.route('/my_page', methods=['GET'])
    @user_app.route('/my_page/<int:seller_id>', methods=['GET'])
    @login_decorator
    def get_seller_information(**seller_id):
        """
        셀러 상세정보 가져오기
        마스터 토큰으로 seller_id 파라미터가 없을 시 require parameter
        셀러 토큰으로 seller_id 파라미터 적용 시 permission denied
        :return: 셀러 상세정보
        """

        db = None
        try:
            db = db_connection()

            # 마스터
            if request.is_master:
                if not seller_id:
                    return jsonify({'message' : 'require parameter'}), 400

                seller_id = seller_id['seller_id']
            # 셀러
            else:
                if seller_id:
                    return jsonify({'message': 'permission denied'}), 403

                seller_id = request.seller_id

            seller_info = user_service.get_seller_information(db, seller_id)

            return jsonify({'message' : 'success', 'seller_info': seller_info}), 200
        except NotExistsException as e:
            return jsonify({'message' : e.message}), e.status_code
        except Exception as e:
            return jsonify({'message' : 'error {}'.format(e)}), 500
        finally:
            if db:
                db.close()

    @user_app.route('/my_page', methods=['PUT'])
    @user_app.route('/my_page/<int:seller_id>', methods=['PUT'])
    @login_decorator
    def update_seller_information(**seller_id):
        """
        셀러 상세정보 수정
        마스터 토큰으로 seller_id 파라미터가 없을 시 require parameter
        셀러 토큰으로 seller_id 파라미터 적용 시 permission denied
        :param seller_id: seller_id
        """

        db = None
        try:
            data = request.json
            db = db_connection()

            # 마스터
            if request.is_master:
                if not seller_id:
                    return jsonify({'message' : 'require parameter'}), 400

                seller_id = seller_id['seller_id']
                modifier_id = request.seller_id
            # 셀러
            else:
                if seller_id:
                    return jsonify({'message': 'permission denied'}), 403

                seller_id = request.seller_id
                modifier_id = request.seller_id

            user_service.update_seller_information(db, data, seller_id, modifier_id)

            db.commit()

            return jsonify({'message' : 'success'}), 200
        except KeyError as e:
            db.rollback()
            return jsonify({'message' : 'key_error {}'.format(e)}), 400
        except Exception as e:
            db.rollback()
            return jsonify({'message' : 'error {}'.format(e)}), 500
        finally:
            if db:
                db.close()

    @user_app.route('/<int:seller_id>', methods=['PATCH'])
    @login_decorator
    def update_shop_status(seller_id):
        """
        셀러 상태(입점상태) 수정
        마스터 토큰이 아닐 시 permission denied
        :param seller_id: seller_id
        """

        db = None
        try:
            data = request.json
            db = db_connection()

            if not request.is_master:
                return jsonify({'message' : 'permission denied'}), 403

            user_service.update_shop_status(db, data, seller_id)

            db.commit()

            return jsonify({'message' : 'success'}), 200
        except NotExistsException as e:
            db.rollback()
            return jsonify({'message' : e.message}), e.status_code
        except InvalidValueException as e:
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

    @user_app.route('/my_page/manager', methods=['POST'])
    @user_app.route('/my_page/<int:seller_id>/manager', methods=['POST'])
    @login_decorator
    def create_manager(**seller_id):
        """
        담당 매니저 생성
        :param seller_id: seller_id
        """

        db = None
        try:
            data = request.json
            db = db_connection()

            # 마스터
            if request.is_master:
                if not seller_id:
                    return jsonify({'message' : 'require parameter'}), 400

                seller_id = seller_id['seller_id']
            # 셀러
            else:
                if seller_id:
                    return jsonify({'message': 'permission denied'}), 403

                seller_id = request.seller_id

            user_service.create_managers(db, data, seller_id)
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

    @user_app.route('my_page/history', methods=['GET'])
    @user_app.route('my_page/<int:seller_id>/history', methods=['GET'])
    @login_decorator
    def get_seller_status_log(**seller_id):
        """
        셀러 상세 히스토리 정보 조회
        :param seller_id: seller_id
        :return: 상세 히스토리 리스트(시간, 입점상태, 수정자)
        """

        db = None
        try:
            db = db_connection()

            if request.is_master:
                if not seller_id:
                    return jsonify({'message' : 'require parameter'}), 400

                seller_id = seller_id['seller_id']
            else:
                if seller_id:
                    return jsonify({'message': 'permission denied'}), 403

                seller_id = request.seller_id

            log_list = user_service.get_seller_status_log(db, seller_id)

            return jsonify({'message' : 'success', 'log_list' : log_list}), 200
        except Exception as e:
            return jsonify({'message' : 'error {}'.format(e)}), 500
        finally:
            if db:
                db.close()

    def upload_files():
        db = None
        try:
            db = db_connection()
        except Exception as e:
            return jsonify({'message' : 'error {}'.format(e)}), 500
        finally:
            if db:
                db.close()

    return user_app
