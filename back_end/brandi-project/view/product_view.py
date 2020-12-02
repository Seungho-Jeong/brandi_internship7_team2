from flask          import Blueprint, request, jsonify

from util.exception import NotExistsException
from db_connection  import db_connection
from util.decorator import login_decorator

def product_endpoints(product_service):
    product_app = Blueprint('product_app', __name__, url_prefix='/product')

    @product_app.route('/<int:product_id>', methods=['GET'])
    @login_decorator
    def view_product_information(product_id):
        """
        상품 아이디가 주어지면 상품에 대한 상세정보를 JSON 형식으로 Response하는 함수입니다
        :param product_id: 상품 아이디(ID)
        :return:
            200: 상품 상세정보
            500: Exception message
        """

        db = None
        try:
            db = db_connection()

            product_info = product_service.get_product_information(db, product_id)

            return jsonify({'message': 'success', 'product_detail' : product_info}), 200
        except NotExistsException as e:
            return jsonify({'message': e.message}), e.status_code
        except Exception as e:
            return jsonify({'message': 'error {}'.format(e)}), 500
        finally:
            if db:
                db.close()

    @product_app.route('/registration', methods=['POST'])
    @login_decorator
    def registrate_new_product():
        """
        신규 상품에 대한 정보가 JSON형식으로 주어지면 DB에 입력하는 함수입니다
        :return:
            200: Success mesaage, 신규 등록 상품 아이디(ID)
            400: Key error message
            500: Exception message
        """

        db = None
        try:
            db           = db_connection()
            product_info = request.json

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
            200: Success message, 대상 상품 아이디(ID)
            400: Key error message
            500: Exception message
        """

        db = None
        try:
            db          = db_connection()
            update_data = request.json

            seller_id                 = request.seller_id
            update_data['seller_id']  = seller_id
            update_data['product_id'] = product_id

            product_service.update_product_information(db, update_data)
            db.commit()

            return jsonify({'message' : 'success', 'product_id' : product_id}), 200
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

