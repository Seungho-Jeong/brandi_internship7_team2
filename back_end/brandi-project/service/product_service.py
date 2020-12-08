from PIL import Image

from flask          import current_app
from datetime       import date, datetime

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

        ## 관리자 계정이 아닌 경우 자신이 보유한 상품인지 검사
        if search_params['seller_id']:
            if not self.product_dao.select_match_product_and_seller(db, search_params):
                raise InvalidValueException('product inquiry failed', 401)

        product_info   = self.product_dao.select_product_information(db, search_params)
        product_images = self.product_dao.select_product_image(db, search_params)

        product_detail = {
            'product_info' : product_info,
            'product_image': [dict(image) for image in product_images]
        }

        if not product_detail:
            raise NotExistsException('not exists product', 400)

        return product_detail

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

    def get_product_color_size_country(self, db):
        """
        상품 카테고리(1차 카테고리)를 가져오는 함수입니다.
        :param db: 데이터베이스 연결 객체
        :return: 카테고리 리스트(JSON)
        """

        size_list     = self.product_dao.select_product_size(db)
        color_list    = self.product_dao.select_product_color(db)
        country_list  = self.product_dao.select_product_country(db)

        color_size_country_list = {
            'sizes'    : [dict(size) for size in size_list],
            'colors'   : [dict(color) for color in color_list],
            'countries': [dict(country) for country in country_list]
        }

        return color_size_country_list

    def create_new_product(self, db, product_info):
        """
        상품을 새로 생성하는 함수입니다
        :param db: 데이터베이스 연결객체
        :param product_info: 신규 상품 정보
        :return: 신규 등록 상품 ID
        """

        ## 1. 신규 상품 Insert 후 new_product_id 생성
        new_product_id = self.product_dao.insert_product_information(db, product_info)

        ## 2. 할인 기간이 유한하면 할인기간을 Insert
        if product_info['discount_start_date'] or product_info['discount_end_date']:
            product_info['product_id'] = new_product_id
            self.product_dao.insert_product_discount_info(db, product_info)

        ## 5. 제조정보
        if product_info['manufacturing_country_id']:
            product_info['product_id'] = new_product_id
            self.product_dao.insert_product_manufacturing_information(db, product_info)

        ## 3. 각 옵션 & Ordering Number Insert 후 option_id 생성
        ordering = 1
        for size in product_info['sizes']:
            for color in product_info['colors']:
                product_info['product_id']      = new_product_id
                product_info['size_id']         = size
                product_info['color_id']        = color
                product_info['option_ordering'] = ordering

                option_id = self.product_dao.insert_product_option(db, product_info)
                ordering += 1

                ## 4. 각 옵션에 대한 재고수량 Insert(미입력 시 Null)
                for inventory in product_info['inventories']:
                    product_info['option_id']    = option_id
                    product_info['inventory_id'] = inventory
                    self.product_dao.insert_product_inventory(db, product_info)

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

    def upload_product_image(self, s3, product_images, new_product_id):
        image_urls = []

        for product_image in product_images:
            s3.put_object(
                Bucket             = BUCKET_NAME,
                Body               = product_image,
                Key                = f'{new_product_id}_{product_image.filename}',
                ContentType        = product_image.content_type,
                ContentDisposition = 'attachment'
            )
            location  = s3.get_bucket_location(Bucket = BUCKET_NAME)['LocationConstraint']
            image_url = f'https://{BUCKET_NAME}.s3.{location}.amazonaws.com/images/product/{new_product_id}/{datetime.now()}_{product_image.filename}'
            image_urls.append(image_url)

        return image_urls

    def create_product_image_url(self, db, product_info, image_urls):

        ordering = 1
        for image_url in image_urls:
            product_info['image_url']      = image_url
            product_info['image_ordering'] = ordering

            self.product_dao.insert_product_image(db, product_info)
            ordering += 1