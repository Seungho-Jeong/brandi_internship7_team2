import json

from flask import Blueprint, request, jsonify
from PIL   import Image

from util.exception import (
    ALLOWED_EXTENSIONS,
    ExistsException,
    NotExistsException,
    InvalidValueException,
    PermissionException,
    PathParameterException,
    FileException,
    RequestException
)
from util.validation import KeywordValidation
from db_connection   import db_connection, s3_connection
from util.decorator  import login_decorator
from werkzeug.exceptions import RequestEntityTooLarge


def user_endpoints(user_service):
    user_app = Blueprint('user_app', __name__, url_prefix='/user')
    keyword_validation = KeywordValidation()

    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    @user_app.route('/signup', methods=['POST'])
    def sign_up():
        """
        유저 회원가입
        """

        db = None
        try:
            db = db_connection()
            data = request.json

            if not data:
                raise RequestException
            # key_error 예외처리
            keyword_validation.signup(data)

            user_service.sign_up(db, data)
            db.commit()

            return jsonify({'message' : 'success'}), 200
        except RequestException as e:
            db.rollback()
            return jsonify({'message' : e.message}), e.status_code
        except ExistsException as e:
            db.rollback()
            return jsonify({'message' : e.message}), e.status_code
        except KeyError as e:
            db.rollback()
            return jsonify({'message': format(e)}), 400
        except Exception as e:
            db.rollback()
            return jsonify({'message' : '서버 오류 : {}'.format(e)}), 500
        finally:
            if db:
                db.close()

    @user_app.route('/signin', methods=['POST'])
    def sign_in():
        """
        유저 로그인
        account, password
        :return: access_token
        """

        db = None
        try:
            db = db_connection()
            data = request.json

            if not data:
                raise RequestException
            # key_error 예외처리
            keyword_validation.signin(data)

            access_token = user_service.sign_in(db, data)
            db.commit()

            return jsonify({'message' : 'success', 'access_token' : access_token}), 200
        except RequestException as e:
            db.rollback()
            return jsonify({'message' : e.message}), e.status_code
        except PermissionException as e:
            db.rollback()
            return jsonify({'message' : e.message}), e.status_code
        except NotExistsException as e:
            db.rollback()
            return jsonify({'message' : e.message}), e.status_code
        except KeyError as e:
            db.rollback()
            return jsonify({'message': format(e)}), 400
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
                raise PermissionException

            filter_list = ['id', 'account', 'name_en', 'name_ko',
                           'manager_name', 'manager_mobile', 'manager_email',
                           'category', 'start_date', 'end_date',
                           'offset', 'limit']

            filters = dict(request.args)

            for key in filters:
                if key not in filter_list:
                    return jsonify({'message' : "검색 필터의 '{}'은 잘못된 값입니다.".format(key)}), 400

            if ('start_date' in filters) and ('end_date' in filters):
                if filters['end_date'] < filters['start_date']:
                    raise InvalidValueException("'종료 날짜'가 '시작 날짜'보다 이전의 날짜일 수 없습니다.", 400)

            if ('offset' in filters) and (int(filters['offset']) <= 0):
                raise InvalidValueException("페이지 번호는 1보다 크거나 같은 정수여야 합니다.", 400)

            if ('limit' in filters) and (int(filters['limit']) <= 0):
                raise InvalidValueException("페이지 행의 개수는 1보다 크거나 같은 정수여야 합니다.", 400)

            sellers = user_service.get_seller_list(db, filters)

            return jsonify({'message' : 'success', 'total_count' : sellers['count'],
                            'seller_list' : sellers['seller_list']}), 200

        except PermissionException as e:
            return jsonify({'message' : e.message}), e.status_code
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
                    raise PathParameterException('seller_id')

                seller_id = seller_id['seller_id']
            # 셀러
            else:
                if seller_id:
                    raise PermissionException

                seller_id = request.seller_id

            seller_info = user_service.get_seller_information(db, seller_id)

            return jsonify({'message' : 'success', 'seller_info': seller_info}), 200
        except PathParameterException as e:
            return jsonify({'message' : e.message}), e.status_code
        except PermissionException as e:
            return jsonify({'message' : e.message}), e.status_code
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
            db = db_connection()
            s3 = s3_connection()
            form_data = dict(request.form)

            if not form_data:
                raise RequestException

            data = json.loads(form_data['body'])

            # 파일 확장자 확인
            if request.files:
                profile_image = request.files['profile_image'] if 'profile_image' in request.files else None
                if profile_image and not allowed_file(profile_image.filename):
                    raise FileException('해당 파일의 확장자는 사용할 수 없습니다.', 400)
                data['profile_image'] = profile_image if profile_image.filename else None

                background_image = request.files['background_image'] if 'background_image' in request.files else None
                if background_image and not allowed_file(background_image.filename):
                    raise FileException('해당 파일의 확장자는 사용할 수 없습니다.', 400)
                data['background_image'] = background_image if background_image.filename else None

                # 파일 size (width, height) 확인
                if background_image:
                    image = Image.open(background_image)
                    width, height = image.size

                    if width < 1200 or height < 850:
                        raise FileException('배경이미지의 크기는 가로 1200, 세로 850 이상이어야 합니다.', 400)

                    # 파일 스트림 포인터를 다시 초기화
                    background_image.seek(0)

            # key_error 예외처리
            keyword_validation.update_seller_information(data)

            # 마스터
            if request.is_master:
                if not seller_id:
                    raise PathParameterException('seller_id')

                seller_id = seller_id['seller_id']
                modifier_id = request.seller_id
            # 셀러
            else:
                if seller_id:
                    raise PermissionException

                seller_id = request.seller_id
                modifier_id = request.seller_id

            user_service.update_seller_information(db, data, s3, seller_id, modifier_id)

            db.commit()

            return jsonify({'message' : 'success'}), 200
        except RequestException as e:
            db.rollback()
            return jsonify({'message' : e.message}), e.status_code
        except RequestEntityTooLarge:
            db.rollback()
            return jsonify({'message' : '이미지 파일의 크기는 5MB 이하여야 합니다.'}), 400
        except FileException as e:
            db.rollback()
            return jsonify({'message' : e.message}), e.status_code
        except PathParameterException as e:
            db.rollback()
            return jsonify({'message' : e.message}), e.status_code
        except InvalidValueException as e:
            db.rollback()
            return jsonify({'message' : e.message}), e.status_code
        except PermissionException as e:
            db.rollback()
            return jsonify({'message' : e.message}), e.status_code
        except KeyError as e:
            db.rollback()
            return jsonify({'message' : 'key_error {}'.format(e)}), 400
        except Exception as e:
            db.rollback()
            return jsonify({'message' : '{}'.format(e)}), 500
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
            db = db_connection()
            data = request.json

            if not data:
                raise RequestException
            # key_error 예외처리
            keyword_validation.update_shop_status(data)

            if not request.is_master:
                raise PermissionException

            user_service.update_shop_status(db, data, seller_id)

            db.commit()

            return jsonify({'message' : 'success'}), 200
        except RequestException as e:
            db.rollback()
            return jsonify({'message' : e.message}), e.status_code
        except PermissionException as e:
            db.rollback()
            return jsonify({'message' : e.message}), e.status_code
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
            return jsonify({'message' : '{}'.format(e)}), 500
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
                    raise PathParameterException('seller_id')

                seller_id = seller_id['seller_id']
            else:
                if seller_id:
                    raise PermissionException

                seller_id = request.seller_id

            log_list = user_service.get_seller_status_log(db, seller_id)

            return jsonify({'message' : 'success', 'log_list' : log_list}), 200
        except PathParameterException as e:
            return jsonify({'message' : e.message}), e.status_code
        except PermissionException as e:
            return jsonify({'message' : e.message}), e.status_code
        except Exception as e:
            return jsonify({'message' : '{}'.format(e)}), 500
        finally:
            if db:
                db.close()

    return user_app
