import jwt
import bcrypt
from datetime import datetime, timedelta

from util.exception import NotExistsException, InvalidValueException
from config         import SECRET, ALGORITHM


class ProductService:
    def __init__(self, product_dao):
        self.product_dao = product_dao

    def get_product_information(self, db, search_params):
        """
        주어진 조건(상품 ID, 셀러 ID)에 맞추어 상품 상세정보를 가져오는 함수입니다
        :param search_params: 가져올 상품에 대한 조건 매개변수(product_id, seller_id, is_master)
        :param db: 데이터베이스 연결객체
        :return: 상품 상세정보(JSON)
        """

        if search_params['seller_id']:
            if not self.product_dao.match_check_product_and_seller(db, search_params):
                raise InvalidValueException('product inquiry failed', 401)

        product_info = self.product_dao.get_product_information(db, search_params)

        if not product_info:
            raise NotExistsException('not exists product', 400)

        return product_info

    def create_new_product(self, db, product_info):
        """
        상품을 새로 생성하는 함수입니다
        :param db: 데이터베이스 연결객체
        :param product_info: 신규 상품 정보
        :return: 신규 등록 상품 ID
        """

        new_product_id = self.product_dao.insert_product(db, product_info)

        return new_product_id

    def update_product_information(self, db, update_data):
        """
        상품 정보를 수정하는 함수입니다
        :param db: 데이터베이스 연결 객체
        """

        self.product_dao.update_product_info(db, update_data)

    def get_product_category(self, db, seller_id):
        """
        상품 카테고리(1차 카테고리)를 가져오는 함수입니다.
        :param seller_id:
        :param db: 데이터베이스 연결 객체
        :return: 카테고리 리스트(JSON)
        """

        category_list = self.product_dao.get_product_category(db, seller_id)
        return category_list

    def get_product_subcategory(self, db, category_id):
        """
        상품의 카테고리(1차 카테고리) ID가 주어지면 서브 카테고리(2차 카테고리)를 가져오는 함수입니다.
        :param db: 데이터베이스 연결 객체
        :param category_id: 카테고리 ID (product_category_id)
        :return: 서브 카테고리 리스트
        """

        subcategory_id = self.product_dao.get_product_subcategory(db, category_id)
        return subcategory_id