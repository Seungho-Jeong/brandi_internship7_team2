from PIL import Image

from datetime       import datetime, timedelta, date

from util.exception import NotExistsException, InvalidValueException
from config         import SECRET, ALGORITHM, BUCKET_NAME


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
            if not self.product_dao.select_match_product_and_seller(db, search_params):
                raise InvalidValueException('product inquiry failed', 401)

        product_info = self.product_dao.select_product_information(db, search_params)

        if not product_info:
            raise NotExistsException('not exists product', 400)

        return product_info

    def get_product_seller(self, db, seller_name):
        """
        관리자가 상품을 등록할 경우...
        :param db: 데이터베이스 연결 객체
        :param seller_name: 셀러 국문이름(KO)
        :return: 셀러 ID
        """
        seller_id = self.product_dao.select_product_seller(db, seller_name)

        return seller_id

    def get_product_category(self, db, seller_id):
        """
        상품의 카테고리(1차 카테고리) ID가 주어지면 서브 카테고리(2차 카테고리)를 가져오는 함수입니다.
        :param seller_id:
        :param db: 데이터베이스 연결 객체
        :return: 서브 카테고리 리스트
        """

        subcategory_id = self.product_dao.select_product_category(db, seller_id)

        return subcategory_id

    def get_product_subcategory(self, db, search_params):
        """
        상품의 카테고리(1차 카테고리) ID가 주어지면 서브 카테고리(2차 카테고리)를 가져오는 함수입니다.
        :param search_params:
        :param db: 데이터베이스 연결 객체
        :return: 서브 카테고리 리스트
        """

        inspection_result = self.product_dao.select_match_product_category_and_seller(db, search_params)
        if not inspection_result:
            raise NotExistsException('category inquiry failed', 401)

        subcategory_id = self.product_dao.select_product_subcategory(db, search_params)

        return subcategory_id

    def get_product_color_size(self, db):
        """
        상품 카테고리(1차 카테고리)를 가져오는 함수입니다.
        :param db: 데이터베이스 연결 객체
        :return: 카테고리 리스트(JSON)
        """

        color_list    = self.product_dao.select_product_color(db)
        size_list     = self.product_dao.select_product_size(db)

        color_size_list = {
            'colors' : [dict(color) for color in color_list],
            'sizes'  : [dict(size) for size in size_list]
        }

        return color_size_list

    def create_new_product(self, db, product_info):
        """
        상품을 새로 생성하는 함수입니다
        :param db: 데이터베이스 연결객체
        :param product_info: 신규 상품 정보
        :return: 신규 등록 상품 ID
        """

        ## 상품명이 100자를 초과하는 경우 Error raise
        if len(product_info['product_name']) > 100:
            raise InvalidValueException('product name too long')

        ## 옵션의 수(sizes by colors)와 재고가 일치하지 않으면 Error raise
        if len(product_info['sizes']) * len(product_info['colors']) != len(product_info['inventories']):
            raise InvalidValueException('not match options and inventories', 400)

        ## 최소 발주수량이 있는 경우 : 20개 이상으로 지정하면 Error raise
        if product_info['min_sale_quantity']:
            if product_info['min_sale_quantity'] > 20:
                raise InvalidValueException('minimum quantity({}) exceed 20'.format(product_info['min_sale_quantity']), 400)

        ## 최대 발주수량이 있는 경우 : 20개 이상으로 지정하면 Error raise
        if product_info['max_sale_quantity']:
            if product_info['max_sale_quantity'] > 20:
                raise InvalidValueException('maximum quantity({}) exceed 20'.format(product_info['max_sale_quantity']), 400)

        ## 최소/최대 발주수량이 있는 경우 : 최소 발주수량이 최대 발주수량보다 크면 Error raise
            if product_info['min_sale_quantity']:
                if product_info['min_sale_quantity'] > product_info['max_sale_quantity']:
                    raise InvalidValueException('minimum quantity bigger than maximum', 400)

        ## 1줄 상품소개가 있는 경우 : 100자를 초과하면 Error raise
        if product_info['short_introduction']:
            if len(product_info['short_introduction']) > 100:
                raise InvalidValueException('short_introduction too long')


        ## 1. 신규 상품 Insert 후 new_product_id 생성
        new_product_id = self.product_dao.insert_product_information(db, product_info)

        ## 2. 각 옵션 & Ordering Number Insert 후 option_id 생성
        ordering = 1
        for size in product_info['sizes']:
            for color in product_info['colors']:
                product_info['product_id']      = new_product_id
                product_info['size_id']         = size
                product_info['color_id']        = color
                product_info['option_ordering'] = ordering

                option_id = self.product_dao.insert_product_option(db, product_info)
                ordering += 1

        ## 3. 각 옵션에 대한 재고수량 Insert(미입력 시 Null)
                for inventory in product_info['inventories']:
                    product_info['option_id']    = option_id
                    product_info['inventory_id'] = inventory
                    self.product_dao.insert_product_inventory(db, product_info)

        ## 4. 할인정보 기간이 있는 경우(할인율만 있고 기간이 없는 경우 무기한 할인으로 저장)
        if product_info['discount_start_date'] or product_info['discount_end_date']:
            if not product_info['discount_start_date'] or not ['discount_start_date']:
                raise InvalidValueException('must have both start and end date', 400)

            if date.fromisoformat(product_info['discount_start_date']) > date.fromisoformat(product_info['discount_end_date']):
                raise InvalidValueException('there end date precedes the start date', 400)

            self.product_dao.insert_product_discount_info(db, product_info)

        return new_product_id

    def update_product_information(self, db, modify_data, is_master):
        """
        상품 정보를 수정하는 함수입니다
        :param is_master: 관리자 계정 여부(Bool)
        :param modify_data: 수정 대상 상품에 대한 정보
        :param db: 데이터베이스 연결 객체
        """

        ## 셀러 계정인 경우 : 대상 상품 보유여부 및 존재여부 확인
        if not is_master:
            if not self.product_dao.select_match_product_and_seller(db, modify_data):
                raise InvalidValueException('product inquiry failed', 401)

        ## 관리자 계정인 경우 : 대상 상품 존재여부 확인
        else:
            if not self.product_dao.select_product_information(db, modify_data):
                raise NotExistsException('not exists product', 400)

        modify_result = self.product_dao.update_product_info(db, modify_data)

        if not modify_result:
            raise InvalidValueException('no information change', 400)

        return  modify_result

    # def upload_product_images(self, db, s3, images):
    #     product_image = {}
    #     try:
    #         for idx in range(1,6):
    #             if images.get('product_image_{}'.format(idx), None) is not None:
    #                 product_image[images['product_image_{}'.format(idx)].name] = images.get('product_image_{}', None)
    #     return product_image