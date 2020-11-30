import jwt
import bcrypt
from datetime import datetime, timedelta

from util.exception import NotExistsException, ExistsException
from config         import SECRET, ALGORITHM


class ProductService:
    def __init__(self, product_dao):
        self.product_dao = product_dao

    def get_product_information(self, db, product_id):
        """
        상품 상세정보 불러오기
        :param db: 데이터베이스 연결객체
        :param product_id: 상품 아이디(ID)
        :return: 상품 상세정보
        """

        product_info = self.product_dao.get_product_information(db, product_id)

        if not product_info:
            raise NotExistsException('not exists product', 400)

        return product_info

    def create_new_product(self, db, product_info):
        """
        신규 상품 등록
        :param db: 데이터베이스 연결객체
        :param product_info: 신규 상품 정보
        :return: 신규 등록 상품 아이디(ID)
        """

        new_product_id = self.product_dao.insert_product(db, product_info)

        return new_product_id