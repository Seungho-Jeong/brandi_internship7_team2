import json
import re

from flask              import Blueprint, request, jsonify
from datetime           import date

from util.exception     import (
    ALLOWED_EXTENSIONS,
    FileException,
    InvalidValueException,
    NotExistsException,
    PathParameterException,
    PermissionException
)

from db_connection      import db_connection, s3_connection
from util.decorator     import login_decorator
from util.validation    import KeywordValidation

def product_endpoints(product_service):
    product_app = Blueprint('product_app', __name__, url_prefix='/product')
    keyword_validation = KeywordValidation()

    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    @product_app.route('/<int:product_id>', methods=['GET'])
    @login_decorator
    def get_product_information(product_id):
        """
        상품 아이디가 주어지면 조회자가 관리자인지 일반 셀러인지 구분한 뒤
        조회권한이 있는 상품에 대한 상세정보를 JSON 형식으로 Response하는 함수입니다
        :param product_id: 상품 ID
        :return:
            200: 상품 상세정보(JSON)
            400: Path parameter error message
            500: Not exist error message
        """

        db = None
        try:
            db            = db_connection()
            search_params = {}

            ## 숫자가 아닌 값으로 접근하려는 경우
            if re.compile('[\D]').search(str(product_id)):
                raise PathParameterException('product_id is integer only', 400)

            if request.is_master:
                search_params['seller_id']  = None
                search_params['product_id'] = product_id

            else:
                search_params['seller_id']  = request.seller_id
                search_params['product_id'] = product_id

            product_info = product_service.get_product_information(db, search_params)
            return jsonify({'message' : 'success', 'product_detail' : product_info}), 200
        except NotExistsException as e:
            return jsonify({'message' : e.message}), e.status_code
        except Exception as e:
            return jsonify({'message' : 'error {}'.format(e)}), 500
        finally:
            if db:
                db.close()

    @product_app.route('/registration/search_user', methods=['GET'])
    @login_decorator
    def get_search_user():
        """
        관리자가 판매자를 대신하여 상품 신규등록을 대행하는 경우
        대상 상품의 판매자를 검색할 수 있도록 하는 함수입니다
        :return:
            200: 판매자 ID
            401: Permission error message
            500: Not exist error message
        """
        db = None
        try:
            db = db_connection()

            ## 일반 셀러가 접근하려고 하는 경우
            if not request.is_master:
                raise PermissionException('does not have a permission', 401)

            seller_name = request.json['seller_name_ko']
            seller_id   = product_service.get_product_seller(db, seller_name)

            return jsonify({'message' : 'success', 'seller_id' : seller_id})
        except NotExistsException as e:
            return jsonify({'message' : e.message}), e.status_code
        except Exception as e:
            return jsonify({'message' : 'error {}'.format(e)}), 500
        finally:
            if db:
                db.close()

    @product_app.route('/category', methods=['GET'])
    @login_decorator
    def get_product_category_list():
        """
        로그인 토큰에서 셀러 ID를 받아 매칭되는
        상품의 카테고리(1차 카테고리)를 가져오는 함수입니다
        :return:
            200: 카테고리 리스트(JSON, List)
            500: Exception error message
        """

        db = None
        try:
            db = db_connection()

            if request.is_master:
                seller_id = request.json['seller_id']
            else:
                seller_id = request.seller_id

            category_list = product_service.get_product_category(db, seller_id)
            return jsonify({'message' : 'success', 'category_list' : category_list}), 200
        except Exception as e:
            return jsonify({'message' : 'error {}'.format(e)}), 500
        finally:
            if db:
                db.close()

    @product_app.route('/category/<int:category_id>', methods=['GET'])
    @login_decorator
    def get_product_subcategory_list(category_id):
        """
        상품의 카테고리(1차 카테고리) ID가 주어지면 서브 카테고리(2차 카테고리)를 가져오는 함수입니다
        :param category_id: 카테고리 ID (product_category_id)
        :return:
            200: 서브 카테고리 리스트(JSON, List)
            500: Exception error message
        """

        db = None
        try:
            db = db_connection()
            search_params = {}

            ## 숫자가 아닌 값으로 접근하려는 경우
            if re.compile('[\D]').search(str(category_id)):
                raise PathParameterException('category_id is integer only', 400)

            if request.is_master:
                search_params['seller_id']   = request.json['seller_id']
                search_params['category_id'] = category_id

            else:
                search_params['seller_id']   = request.seller_id
                search_params['category_id'] = category_id

            sub_category_list = product_service.get_product_subcategory(db, search_params)
            return jsonify({'message' : 'success', 'subcategory_list' : sub_category_list}), 200
        except KeyError as e:
            return jsonify({'message' : 'key_error {}'.format(e)}), 400
        except Exception as e:
            return jsonify({'message' : 'error {}'.format(e)}), 500
        finally:
            if db:
                db.close()

    @product_app.route('/registration', methods=['GET', 'POST'])
    @login_decorator
    def registrate_new_product():
        """
        신규 상품에 대한 정보가 JSON형식으로 주어지면 DB에 입력하는 함수입니다

        method가 GET인 경우 상품 등록을 위한 페이지에 연결하고,
        method가 POST인 경우 DB에 상품 등록을 실행합니다.
        :return:
            200: Success mesaage, 신규 등록 상품 ID
            400: Key error message
            500: Exception error message
        """

        if request.method == 'GET':
            db = None
            try:
                db = db_connection()

                ## 색상, 사이즈, 제조국 List
                property_list = product_service.get_product_color_size_country(db)

                return jsonify({'message' : 'success', 'product_detail': property_list}), 200
            except Exception as e:
                return jsonify({'message' : 'error {}'.format(e)}), 500
            finally:
                if db:
                    db.close()

        else:
            db = None
            try:
                form_data    = dict(request.form)
                product_info = json.loads(form_data['body'])
                seller_id    = request.seller_id
                is_master    = request.is_master

                if not is_master:
                    product_info['seller_id'] = seller_id

                # keyword_validation.create_new_product(product_info)

                ## 옵션 정보가 없는 경우
                if product_info['sizes'] is None or product_info['colors'] is None:
                    raise NotExistsException('not exists option data', 400)

                ## 상품명에 따옴표 또는 쌍따옴표가 있는 경우
                if re.compile('[\"\']').search(product_info['product_name']):
                    raise InvalidValueException('product name invalied', 400)

                ## 상품명이 100자를 초과하는 경우
                if len(product_info['product_name']) > 100:
                    raise InvalidValueException('product name too long', 400)

                ## 옵션의 수(sizes by colors)와 재고가 일치하지 않는 경우
                if len(product_info['sizes']) * len(product_info['colors']) != len(product_info['inventories']):
                    raise InvalidValueException('not match options and inventories', 400)

                ## 최소 발주수량이 20개 이상인 경우
                if product_info['min_sale_quantity']:
                    if product_info['min_sale_quantity'] > 20:
                        raise InvalidValueException(
                            'minimum quantity({}) exceed 20'.format(product_info['min_sale_quantity']), 400)

                ## 최대 발주수량이 20개 이상인 경우
                if product_info['max_sale_quantity']:
                    if product_info['max_sale_quantity'] > 20:
                        raise InvalidValueException(
                            'maximum quantity({}) exceed 20'.format(product_info['max_sale_quantity']), 400)

                ## 최소 발주수량이 최대 발주수량보다 큰 경우
                    if product_info['min_sale_quantity']:
                        if product_info['min_sale_quantity'] > product_info['max_sale_quantity']:
                            raise InvalidValueException('minimum quantity bigger than maximum', 400)

                ## 제조일자가 오늘보다 미래인 경우
                if product_info['manufacturing_date']:
                    if date.fromisoformat(product_info['manufacturing_date']) > date.today():
                        raise InvalidValueException('invalid manufacturing date', 400)

                ## 1줄 상품소개가 100자를 초과하는 경우
                if product_info['short_introduction']:
                    if len(product_info['short_introduction']) > 100:
                        raise InvalidValueException('short_introduction too long', 400)

                ## 할인율이 음수이거나 100%를 초과하는 경우
                if product_info['discount_ratio']:
                    if product_info['discount_ratio'] not in range(0, 100):
                        return InvalidValueException('discount ratio must be between 0 and 99', 400)

                ## 할인기간이 유한하나 시작날짜 또는 종료날짜만 선택된 경우
                if product_info['discount_start_date'] or product_info['discount_end_date']:
                    if not product_info['discount_end_date'] or not ['discount_start_date']:
                        raise InvalidValueException('must have both start and end date', 400)

                    ## 할인기간 종료날짜가 시작날짜보다 앞서는 경우
                    if date.fromisoformat(product_info['discount_start_date']) > date.fromisoformat(product_info['discount_end_date']):
                        raise InvalidValueException('there end date precedes the start date', 400)

                ## 1. 신규 상품 ID 생성
                db             = db_connection()
                new_product_id = product_service.create_new_product(db, product_info)

                ## 2. 이미지 S3 업로드
                s3             = s3_connection()
                product_images = []

                for idx in range(1, 6):
                    product_image = request.files.get('image_{}'.format(idx), None)

                    if product_image:
                        if allowed_file(product_image.filename) is False:
                            raise FileException('the extension of that file is not available', 400)

                        product_images.append(product_image)
                        image_urls = product_service.upload_product_image(s3, product_images, new_product_id)

                        ## 3. 이미지 url RDB Record
                        product_service.create_product_image_url(db, product_info, image_urls)

                db.commit()

                return jsonify({'message' : 'success', 'product_id' : new_product_id}), 200
            except KeyError as e:
                db.rollback()
                return jsonify({'message' : 'key_error {}'.format(e)}), 400
            except Exception as e:
                db.rollback()
                return jsonify({'message' : 'error {}'.format(e)}), 500
            finally:
                if db:
                    db.close()

    @product_app.route('/modify/<int:product_id>', methods=['GET', 'PUT'])
    @login_decorator
    def modify_product_information(product_id):
        """
        수정하고자 하는 상품의 아이디(ID)와 정보(JSON)가 주어지면 DB에 반영하는 함수입니다
        :param product_id: 대상 상품 아이디(ID)
        :return:
            200: Success message, 대상 상품 ID
            400: Key error message
            500: Exception error message
        """

        if request.method == 'GET':
            db = None
            try:
                db = db_connection()
                search_params = {}

                if request.is_master:
                    search_params['seller_id'] = None
                    search_params['product_id'] = product_id

                else:
                    search_params['seller_id'] = request.seller_id
                    search_params['product_id'] = product_id

                product_info = product_service.get_product_information(db, search_params)
                return jsonify({'message': 'success', 'product_detail': product_info}), 200
            except NotExistsException as e:
                return jsonify({'message': e.message}), e.status_code
            except InvalidValueException as e:
                return jsonify({'message': e.message}), e.status_code
            except Exception as e:
                return jsonify({'message': 'error {}'.format(e)}), 500
            finally:
                if db:
                    db.close()

        else:
            db = None
            try:
                db          = db_connection()
                s3          = s3_connection()

                form_data   = dict(request.form)
                modify_data = json.loads(form_data['body'])

                modify_data['is_master']  = request.is_master
                modify_data['seller_id']  = request.seller_id
                modify_data['product_id'] = product_id

                product_service.update_product_information(db, modify_data)

                db.commit()

                return jsonify({'message' : 'success', 'product_id' : product_id}), 200
            except NotExistsException as e:
                db.rollback()
                return jsonify({'message' : e.message}), e.status_code
            except InvalidValueException as e:
                db.rollback()
                return jsonify({'message': e.message}), e.status_code
            except KeyError as e:
                db.rollback()
                return jsonify({'message' : 'key_error {}'.format(e)}), 400
            except Exception as e:
                db.rollback()
                return jsonify({'message' : 'error {}'.format(e)}), 500
            finally:
                if db:
                    db.close()

    return product_app
