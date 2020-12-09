def validation(data, lst, func_name):
    data_list = []
    # 틀린 key 값을 요청받았을 경우
    for key in data:
        data_list.append(key)
        if key not in lst:
            raise KeyError(f'{func_name}에서 {key}값은 잘못된 키값입니다.')

    # 특정 key 값을 요청하지 않은 경우
    keys = list(set(lst) - set(data_list))
    if keys:
        raise KeyError(f'{func_name}에서 {keys[0]}값이 필요합니다.')


class KeywordValidation:
    # 회원가입
    def signup(self, data):
        lst = [
            'seller_category_id',
            'account',
            'password',
            'manager_mobile',
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
        print(data)
        lst = [
            'seller_id',
            'product_name',
            'price',
            'short_introduction',
            'product_detail_information',
            'discount_ratio',
            'min_sale_quantity',
            'max_sale_quantity',
            'registration_status_id',
            'sale_status_id',
            'display_status_id',
            'discount_start_date',
            'discount_end_date',
            'manufacturing_country_id',
            'manufacturing_date',
            'manufacturing_company',
            'product_subcategory_id',
            'sizes',
            'colors',
            'inventories',
            'product_images'
        ]
        validation(data, lst, '상품 신규 등록')

    def modify_product_information(self, data):
        lst = [
            'product_name',
            'price',
            'short_introduction',
            'product_detail_information',
            'discount_ratio',
            'min_sale_quantity',
            'max_sale_quantity',
            'registration_status_id',
            'sale_status_id',
            'display_status_id',
            'discount_start_date',
            'discount_end_date',
            'manufacturing_country_id',
            'manufacturing_date',
            'manufacturing_company'
        ]
        validation(data, lst, '상품 정보 수정')
