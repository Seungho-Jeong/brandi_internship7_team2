class ProductDao:
    def select_match_product_and_seller(self, db, inspection_data):
        """
        상품 상세정보 보기 또는 Modify를 위하여 상품정보를 Get할 때
        대상 상품이 실존하는지 검사하는 함수입니다.
        :param db: Database connection instance
        :param inspection_data: 대상 상품의 정보
        :return:
        """

        with db.cursor() as cursor:
            cursor.execute("""
                SELECT
                    id
                FROM
                    products
                WHERE
                    id = %(product_id)s
                    AND seller_id = %(seller_id)s
                    AND is_delete = 0
            """, inspection_data)

            return cursor.fetchone()

    def select_product_information(self, db, search_params):
        """
        전달받은 상품 아이디(Params)에 해당하는 정보를 DB Select하는 함수입니다
        :param search_params: 조회대상의 ID(product_id)가 포함된 매개변수
        :param db: Database 연결 객체
        :return: 대상 상품 상세정보
        """

        with db.cursor() as cursor:
            cursor.execute("""
                SELECT
                    p.id,
                    p.product_name,
                    p.price,
                    p.short_introduction,
                    p.product_detail_information,
                    p.discount_ratio,
                    p.min_sale_quantity,
                    p.max_sale_quantity,
                    p.seller_id,
                    p.created_at,
                    p.is_delete,
                    p.registration_status_id,
                    p.sale_status_id,
                    p.display_status_id,
                    p.modifier_id,
                    p.product_subcategory_id,
                    d.discount_start_date,
                    d.discount_end_date,
                    m.manufacturing_country_id,
                    m.manufacturing_date,
                    m.manufacturing_company
                FROM
                    products AS p
                    LEFT JOIN
                        sellers
                        ON p.seller_id = sellers.id
                    LEFT JOIN
                        registration_status_type AS registration
                        ON p.registration_status_id = registration.id
                    LEFT JOIN
                        sale_status_type AS sale
                        ON p.sale_status_id = sale.id
                    LEFT JOIN
                        display_status_type AS display
                        ON p.display_status_id = display.id
                    LEFT JOIN
                        sellers AS seller
                        ON p.modifier_id = seller.id
                    LEFT JOIN
                        product_subcategories_type AS subcat
                        ON p.product_subcategory_id = subcat.id
                    LEFT JOIN
                        discounts AS d
                        ON p.id = d.product_id
                    LEFT JOIN
                        manufacturings AS m
                        ON p.id = m.product_id
                WHERE
                    p.id = %(product_id)s
                    AND p.is_delete = 0
            """, search_params)

            return cursor.fetchone()

    def select_product_image(self, db, search_params):
        """
        상품 상세정보 보기 또는 Modify를 위하여 상품정보를 Get할 때
        대상 상품의 이미지(Max 5개)를 불러오는 함수입니다.
        :param db: Database connection instance
        :param search_params: 대상 상품의 정보
        :return: 이미지 url(S3) 리스트
        """

        with db.cursor() as cursor:
            cursor.execute("""
                SELECT
                    id,
                    product_image
                FROM
                    product_images
                WHERE
                    product_id = %(product_id)s
                    AND is_delete = 0
            """, search_params)

            return cursor.fetchall()

    def select_product_option_and_inventory(self, db, search_params):
        """
        상품 상세정보 보기 또는 Modify를 위하여 상품정보를 Get할 때
        대상 상품의 옵션과 해당 옵션에 대한 재고를 불러오는 함수입니다.
        :param db: Database connection instance
        :param search_params: 대상 상품의 정보
        :return: 옵션 및 재고 리스트
        """

        with db.cursor() as cursor:
            cursor.execute("""
                SELECT
                    o.id AS option_id,
                    i.inventory
                FROM
                    options AS o
                    LEFT JOIN
                        inventory_settings AS i
                        ON o.id = i.option_id
                WHERE
                    o.product_id = %(product_id)s
            """, search_params)

            return cursor.fetchall()

    def select_product_seller(self, db, seller_name):
        """
        관리자가 판매자를 대신하여 상품 신규등록을 대행하는 경우
        대상 상품의 판매자를 선택할 수 있도록 판매자를 검색하는 함수입니다.
        :param db: Database connection instance
        :param seller_name: 판매자 이름(국문)
        :return: 판매자 ID
        """

        with db.cursor() as cursor:
            cursor.execute("""
                SELECT
                    id
                FROM
                    sellers
                WHERE
                    seller_name_ko = %s
            """, seller_name)

            return cursor.fetchone()

    def select_product_category(self, db, seller_id):
        """
        상품의 카테고리(1차 카테고리)를 DB Select하는 함수입니다.
        :param seller_id: 등록할 상품을 보유한 셀러 ID
        :param db: 데이터베이스 연결 객체
        :return: 카테고리 리스트
        """

        with db.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    p_cat.id,
                    p_cat.name
                FROM
                    product_categories_type AS p_cat
                    INNER JOIN
                        seller_categories_type AS s_cat
                        ON s_cat.seller_type_id = p_cat.seller_type_id
                    INNER JOIN
                        sellers AS s
                        ON s.seller_category_id = s_cat.id
                WHERE
                    s.id = %s
            """, seller_id)

            return cursor.fetchall()

    def select_product_subcategory(self, db, search_params):
        """
        상품의 서브 카테고리(2차 카테고리)를 DB Select하는 함수입니다
        :param search_params: 대상 상품의 정보
        :param db: 데이터베이스 연결 객체
        :return: 서브 카테고리 리스트
        """

        with db.cursor() as cursor:
            cursor.execute("""
                SELECT
                    subcat.id,
                    subcat.name
                FROM
                    product_subcategories_type AS subcat
                    INNER JOIN product_categories_type AS cat
                        ON subcat.product_category_id = cat.id
                WHERE
                    cat.id = %(category_id)s
            """, search_params)

            return cursor.fetchall()

    def select_product_color(self, db):
        """
        상품 신규등록 화면(API) 실행 시 표시해야 하는
        옵션 중 색상에 대한 리스트 정보를 불러오는 함수입니다.
        :param db: Database connection instance
        :return: 색상 리스트
        """

        with db.cursor() as cursor:
            cursor.execute("""
                SELECT
                    id,
                    name
                FROM
                    colors_type
            """)

            return cursor.fetchall()

    def select_product_size(self, db):
        """
        상품 신규등록 화면(API) 실행 시 표시해야 하는
        옵션 중 사이즈에 대한 리스트 정보를 불러오는 함수입니다.
        :param db: Database connection instance
        :return: 사이즈 리스트
        """

        with db.cursor() as cursor:
            cursor.execute("""
                SELECT
                    id,
                    name
                FROM
                    sizes_type
            """)

            return cursor.fetchall()

    def select_product_country(self, db):
        """
        상품 신규등록 화면(API) 실행 시 표시해야 하는
        제조정보 중 제조국가에 대한 메타 정보를 불러오는 함수입니다.
        :param db: Database connection instance
        :return: 국가 리스트
        """

        with db.cursor() as cursor:
            cursor.execute("""
                SELECT
                    id,
                    country_name
                FROM
                    countries_type
            """)

            return cursor.fetchall()

    def insert_product_option(self, db, product_info):
        """
        상품 신규등록 과정에서 옵션을 생성하면
        RDB에 해당 상품에 대한 옵션 정보를 Insert하는 함수입니다.
        :param db: Database connection instance
        :param product_info: 해당 상품의 정보
        :return:
        """

        with db.cursor() as cursor:
            cursor.execute("""
                INSERT INTO options (
                    seller_id,
                    product_id,
                    color_id,
                    size_id,
                    option_ordering
                ) VALUES (
                    %(seller_id)s,
                    %(product_id)s,
                    %(color_id)s,
                    %(size_id)s,
                    %(option_ordering)s
                )
            """, product_info)

            return cursor.lastrowid

    def insert_product_inventory(self, db, product_info):
        """
        상품 신규등록 과정에서 옵션을 생성한 뒤
        RDB에 해당 상품의 각 옵션에 대한 재고 관리여부 및 재고수량을 Insert하는 함수입니다.
        :param db: Database connection instance
        :param product_info: 해당 상품의 정보
        :return:
        """

        with db.cursor() as cursor:
            cursor.execute("""
                INSERT INTO inventory_settings(
                    seller_id,
                    product_id,
                    option_id,
                    inventory
                ) VALUES (
                    %(seller_id)s,
                    %(product_id)s,
                    %(option_id)s,
                    %(inventory)s
                )
            """, product_info)

            return cursor.lastrowid

    def insert_product_discount_info(self, db, product_info):
        """
        상품 신규등록 과정에서 할인 정보를 입력한 경우
        RDB에 해당 상품에 대한 할인정보를 Insert하는 함수입니다.
        :param db: Database connection instance
        :param product_info: 해당 상품의 정보
        :return:
        """

        with db.cursor() as cursor:
            cursor.execute("""
                INSERT INTO discounts(
                    seller_id,
                    product_id,
                    discount_start_date,
                    discount_end_date
                ) VALUES (
                    %(seller_id)s,
                    %(product_id)s,
                    %(discount_start_date)s,
                    %(discount_end_date)s
                )
            """, product_info)

            return cursor.lastrowid

    def insert_product_manufacturing_information(self, db, product_info):
        # print(product_info)
        """
        상품 신규등록 과정에서 제조정보를 별도 입력한 경우
        RDB에 해당 상품의 제조정보를 Insert하는 함수입니다.
        :param db: Database connection instance
        :param product_info: 해당 상품의 정보
        :return: 옵션 테이블의 마지막 Record number
        """

        with db.cursor() as cursor:
            cursor.execute("""
                INSERT INTO manufacturings(
                    seller_id,
                    product_id,
                    manufacturing_country_id,
                    manufacturing_date,
                    manufacturing_company
                ) VALUES (
                    %(seller_id)s,
                    %(product_id)s,
                    %(manufacturing_country_id)s,
                    %(manufacturing_date)s,
                    %(manufacturing_company)s
                )
            """, product_info)

    def insert_product_image(self, db, product_info):
        """
        상품 신규등록 과정에서 상품 이미지를 S3 서버에 업로드한 경우
        해당 이미지의 url을 RDB에 해당 상품의 제조정보를 Insert하는 함수입니다.
        :param db: Database connection instance
        :param product_info: 해당 상품의 정보
        :return:
        """

        with db.cursor() as cursor:
            cursor.execute("""
                INSERT INTO product_images (
                    seller_id,
                    product_id,
                    product_image,
                    image_ordering
                ) VALUES (
                    %(seller_id)s,
                    %(product_id)s,
                    %(image_url)s,
                    %(image_ordering)s
                )
            """, product_info)

    def insert_product_information(self, db, product_info):
        """
        전달받은 상품 정보(Params)를 DB에 Insert하는 함수입니다.
        :param db: 데이터베이스 연결 객체
        :param product_info: 신규 상품의 정보
        :return: 신규 등록한 상품의 ID
        """

        with db.cursor() as cursor:
            cursor.execute("""
                INSERT INTO products (
                    product_name,
                    price,
                    short_introduction,
                    product_detail_information,
                    discount_ratio,
                    min_sale_quantity,
                    max_sale_quantity,
                    seller_id,
                    is_delete,
                    registration_status_id,
                    sale_status_id,
                    display_status_id,
                    modifier_id,
                    product_subcategory_id
                ) VALUES (
                    %(product_name)s,
                    %(price)s,
                    DEFAULT,
                    %(product_detail_information)s,
                    DEFAULT,
                    DEFAULT,
                    DEFAULT,
                    %(seller_id)s,
                    DEFAULT,
                    DEFAULT,
                    DEFAULT,
                    DEFAULT,
                    DEFAULT,
                    %(product_subcategory_id)s
                )
            """, product_info)

            return cursor.lastrowid

    def update_product_info(self, db, update_data):
        """
        전달받은 상품 정보(Params)를 DB에 update하는 함수입니다
        :param db: 데이터베이스 연결 객체
        :param update_data: 상품 수정 정보
        """

        with db.cursor() as cursor:
            modify_result = cursor.execute("""
                UPDATE
                    products AS p
                    LEFT JOIN
                        registration_status_type AS registration
                        ON p.registration_status_id = registration.id
                    LEFT JOIN
                        sale_status_type AS sale
                        ON p.sale_status_id = sale.id
                    LEFT JOIN
                        display_status_type AS display
                        ON p.display_status_id = display.id
                    LEFT JOIN
                        sellers AS seller
                        ON p.modifier_id = seller.id
                    LEFT JOIN
                        product_subcategories_type AS subcat
                        ON p.product_subcategory_id = subcat.id
                SET
                    p.product_name               = %(product_name)s,
                    p.price                      = %(price)s,
                    p.short_introduction         = DEFAULT,
                    p.product_detail_information = %(product_detail_information)s,
                    p.discount_ratio             = DEFAULT,
                    p.min_sale_quantity          = DEFAULT,
                    p.max_sale_quantity          = DEFAULT,
                    p.registration_status_id     = %(registration_status_id)s,
                    p.sale_status_id             = %(sale_status_id)s,
                    p.display_status_id          = %(display_status_id)s,
                    p.modifier_id                = %(seller_id)s,
                    p.product_subcategory_id     = %(product_subcategory_id)s
                WHERE
                    p.id = %(product_id)s
            """, update_data)

            return modify_result
