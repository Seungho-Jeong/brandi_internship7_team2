class ProductDao:
    def get_product_information(self, db, product_id):
        """
        전달받은 상품 아이디(Params)에 해당하는 정보를 DB Select하는 함수입니다
        :param db: Database 연결 객체
        :param product_id: 대상 상품 아이디(ID)
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
                sellers ON p.seller_id = sellers.id
            LEFT JOIN
                registration_status_type AS registration ON p.registration_status_id = registration.id
            LEFT JOIN
                sale_status_type AS sale ON p.sale_status_id = sale.id
            LEFT JOIN
                display_status_type AS display ON p.display_status_id = display.id
            LEFT JOIN
                sellers AS seller ON p.modifier_id = seller.id
            LEFT JOIN
                product_subcategories_type AS subcat ON p.product_subcategory_id = subcat.id
            LEFT JOIN
                product_images AS i ON p.id = i.product_id
            WHERE
                p.id = %s
        """, product_id)

        return cursor.fetchone()

    def insert_product(self, db, product_info):
        """
        전달받은 상품 정보(Params)를 DB에 Insert하는 함수입니다.
        :param db: 데이터베이스 연결 객체
        :param product_info: 신규 상품의 정보
        :return: 신규 등록한 상품의 아이디(ID)
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
                    %(registration_status_id)s,
                    %(sale_status_id)s,
                    %(display_status_id)s,
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
            cursor.execute("""
                UPDATE
                    products AS p
                LEFT JOIN
                    registration_status_type AS registration ON p.registration_status_id = registration.id
                LEFT JOIN
                    sale_status_type AS sale ON p.sale_status_id = sale.id
                LEFT JOIN
                    display_status_type AS display ON p.display_status_id = display.id
                LEFT JOIN
                    sellers AS seller ON p.modifier_id = seller.id
                LEFT JOIN
                    product_subcategories_type AS subcat ON p.product_subcategory_id = subcat.id
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