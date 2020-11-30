from flask import Blueprint, request, jsonify

from util.exception import ExistsException, NotExistsException
from db_connection  import db_connection
from util.decorator import login_decorator


def product_endpoints(product_service):
    product_app = Blueprint('product_app', __name__, url_prefix='/product')

    @product_app.route('/<int:product_id>', methods=['GET'])
    def view_product_information(product_id):
        """
        상품 상세정보 가져오기
        :param product_id: 상품 아이디(ID)
        :return: 상품 상세정보
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
    def registrate_new_product():
        """
        신규 상품 등록
        :return: 신규 등록 상품 아이디(ID)
        """
        db = None
        try:
            db           = db_connection()
            product_info = request.json

            new_product_id = product_service.create_new_product(db, product_info)
            db.commit()

            return jsonify({'message' : 'success', 'product_id': new_product_id}), 200
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
