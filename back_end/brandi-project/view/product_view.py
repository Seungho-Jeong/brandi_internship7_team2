from flask          import Blueprint, request, jsonify

from util.exception import NotExistsException, InvalidValueException, PermissionException
from db_connection  import db_connection
from util.decorator import login_decorator

def product_endpoints(product_service):
    product_app = Blueprint('product_app', __name__, url_prefix='/product')

    @product_app.route('/<int:product_id>', methods=['GET'])
    @login_decorator
    def get_product_information(product_id):
        """
        상품 아이디가 주어지면 조회자가 관리자인지 일반 셀러인지 구분한 뒤
        조회권한이 있는 상품에 대한 상세정보를 JSON 형식으로 Response하는 함수입니다
        :param product_id: 상품 ID
        :return:
            200: 상품 상세정보(JSON)
            500: Exception error message
        """

        db = None
        try:
            db            = db_connection()
            search_params = {}

            ## 관리자 계정인 경우 : 모든 상품 조회 가능
            if request.is_master:
                search_params['seller_id']  = None
                search_params['product_id'] = product_id

            ## 일반 계정인 경우 : 자신이 등록한 상품만 조회 가능
            else:
                search_params['seller_id']  = request.seller_id
                search_params['product_id'] = product_id

            product_info = product_service.get_product_information(db, search_params)

            return jsonify({'message' : 'success', 'product_detail' : product_info}), 200
        except NotExistsException as e:
            return jsonify({'message' : e.message}), e.status_code
        except InvalidValueException as e:
            return jsonify({'message' : e.message}), e.status_code
        except Exception as e:
            return jsonify({'message' : 'error {}'.format(e)}), 500
        finally:
            if db:
                db.close()

    @product_app.route('/registration/search_user', methods=['GET'])
    @login_decorator
    def get_search_user():
        db = None
        try:
            db = db_connection()

            if not request.is_master:
                raise PermissionException('invaild access', 401)

            seller_name = request.json['seller_name_ko']

            seller_id = product_service.get_product_seller(db, seller_name)

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
        로그인 토큰에서 셀러 ID를 받아 매칭되는 상품의 카테고리(1차 카테고리)를 가져오는 함수입니다
        :return:
            200: 카테고리 리스트(JSON, List)
            500: Exception error message
        """

        db = None
        try:
            db = db_connection()

            ## 관리자 계정인 경우 : 셀러 ID를 조회/선택하여 입력(JSON)
            if request.is_master:
                seller_id = request.json['seller_id']

            ## 일반 계쩡인 경우 : 로그인 토큰 내 셀러 ID로 카테고리 자동 선택
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

            sub_category_list = product_service.get_product_subcategory(db, category_id)

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

                color_size_list = product_service.get_product_color_size(db)
                return jsonify({'message' : 'success', 'product_detail': color_size_list}), 200
            except Exception as e:
                return jsonify({'message' : 'error {}'.format(e)}), 500
            finally:
                if db:
                    db.close()
        else:
            db = None
            try:
                db           = db_connection()
                product_info = request.json

                ## 일반 계정인 경우 : 셀러 ID = 로그인 토큰의 셀러 ID
                ## 관리자 계정인 경우 : 'get_search_user' 함수로 seller_id를 받아서(JSON) 사용
                if not request.is_master:
                    product_info['seller_id'] = request.seller_id

                new_product_id = product_service.create_new_product(db, product_info)
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

    @product_app.route('/modify/<int:product_id>', methods=['PUT'])
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

        db = None
        try:
            db          = db_connection()
            modify_data = request.json
            is_master   = request.is_master

            modify_data['seller_id']  = request.seller_id
            modify_data['product_id'] = product_id

            product_service.update_product_information(db, modify_data, is_master)
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
