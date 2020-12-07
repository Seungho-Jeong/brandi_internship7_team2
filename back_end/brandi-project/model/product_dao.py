class ProductDao:
    def select_match_product_and_seller(self, db, inspection_data):
        with db.cursor() as cursor:
            cursor.execute("""
                SELECT
                    id
                FROM
                    products
                WHERE
                    id = %(product_id)s
                    AND seller_id = %(seller_id)s
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
                i.product_image
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
                    product_images AS i
                    ON p.id = i.product_id
            WHERE
                p.id = %(product_id)s
        """, search_params)

        return cursor.fetchone()

    def select_product_seller(self, db, seller_name):
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

    def select_match_product_category_and_seller(self, db, search_params):
        with db.cursor() as cursor:
            cursor.execute("""
                SELECT
                    s.id
                FROM
                    sellers AS s
                WHERE
                    s.seller_category_id = %(category_id)s
                    AND s.id = %(seller_id)s
            """, search_params)

            return cursor.fetchall()

    def select_product_subcategory(self, db, search_params):
        """
        상품의 서브 카테고리(2차 카테고리)를 DB Select하는 함수입니다
        :param db: 데이터베이스 연결 객체
        :param category_id: 카테고리 ID (product_category_id)
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
                    subcat.product_category_id = %(category_id)s
            """, search_params)

            return cursor.fetchall()

    def select_product_color(self, db):
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
        with db.cursor() as cursor:
            cursor.execute("""
                SELECT
                    id,
                    name
                FROM
                    sizes_type
            """)

            return cursor.fetchall()

    def insert_product_option(self, db, product_info):
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
                    %(inventory_id)s
                )
            """, product_info)

            return cursor.lastrowid

    def insert_product_discount_info(self, db, product_info):
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

    def insert_product_image(self, db, product_info):
        with db.cursor() as cursor:
            cursor.execute("""
                INSERT INTO product_images (
                    product_id,
                    product_image,
                    seller_id
                ) VALUES (
                    %(product_id)s,
                    %(image_url)s,
                    %(seller_id)s
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
