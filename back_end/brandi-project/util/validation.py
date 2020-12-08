def validation(data, lst, func_name):
    index = 0
    for key in data:
        if key not in lst:
            raise KeyError(f"invalid key '{key}' in '{func_name}'")
        index += 1

    if index != len(lst):
        raise KeyError(f"required key '{key}' in '{func_name}'")


class KeywordValidation:
    # 회원가입
    def signup(self, data):
        lst = [
            'seller_category_id',
            'account',
            'password',
            'seller_name_ko',
            'seller_name_en',
            'cs_contact',
            'is_master'
        ]
        validation(data, lst, '회원가입')

    # 로그인
    def signin(self, data):
        lst = [
            'account',
            'password'
        ]
        validation(data, lst, '로그인')

    # 셀러 상세정보 수정
    def update_seller_information(self, data):
        lst = [
            'profile_image',
            'background_image',
            'short_introduction',
            'long_introduction',
            'zipcode',
            'address',
            'cs_opening_time',
            'cs_closing_time',
            'delivery_information',
            'exchange_refund_information',
            'seller_category_id',
            'cs_contact',
            'shop_status_id',
            'managers'
        ]
        validation(data, lst, '셀러 상세정보 수정')

    # 셀러 상태 수정 (입점상태)
    def update_shop_status(self, data):
        lst = [
            'shop_status_id'
        ]
        validation(data, lst, '입점 상태 수정')

    # 상품 신규 등록
    def create_new_product(self, data):
        lst = [
            'seller_id',
            'product_subcategory_id',
            'product_name',
            'price',
            'manufacturing_country_id',
            'manufacturing_date',
            'manufacturing_company',
            'short_introduction',
            'product_detail_information',
            'discount_ratio',
            'discount_start_date',
            'discount_end_date',
            'min_sale_quantity',
            'max_sale_quantity',
            'registration_status_id',
            'sale_status_id',
            'display_status_id',
            'colors',
            'sizes',
            'inventories'
        ]
        validation(data, lst, '상품 신규 등록')
