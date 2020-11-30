class ProductDao:
    def get_product_information(self, db, product_id):
        """
        상품 상세정보 불러오기
        :param db: 데이터베이스 연결객체
        :param product_id: 상품 아이디(ID)
        :return: 상품 상세정보
        """

        with db.cursor() as cursor:
            cursor.execute("""
            SELECT
                p.id,
                p.product_name,
                floor(p.price) AS price,
                p.short_introduction,
                p.product_detail_information,
                p.discount_ratio,
                p.min_sale_quantity,
                p.max_sale_quantity,
                p.seller_id,
                date_format(p.created_at, "%%Y-%%m-%%d %%H:%%i:%%S") AS created_at,
                p.is_delete,
                p.registration_status_id,
                p.sale_status_id,
                p.display_status_id,
                p.modifier_id,
                p.product_subcategory_id,
                images.product_image
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
                product_images AS images ON p.id = images.product_id
            WHERE
                p.id = %s
        """, product_id)

        return cursor.fetchone()

    def insert_product(self, db, product_info):
        """
        신규 상품 등록
        :param db: 데이터베이스 연결객체
        :param product_info: 신규 상품 정보
        :return:
        """

        print(product_info)

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