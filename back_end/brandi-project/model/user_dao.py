class UserDao:
    def check_account(self, db, data):
        """
        해당 계정의 존재 여부 체크
        :param db: db_connection
        :param data: request body
        :return: 계정이 존재하면 seller_id, 존재하지 않으면 None
        """

        with db.cursor() as cursor:
            cursor.execute("""
                SELECT
                   seller.id,
                   seller.is_master,
                   info.is_delete
                FROM 
                    sellers AS seller
                INNER JOIN
                    sellers_informations AS info ON seller.id = info.seller_id
                WHERE 
                   account = %(account)s
            """, data)

            return cursor.fetchone()

    def sign_up(self, db, data):
        """
        유저 회원가입
        :param db: db_connection
        :param data: request body
        """

        with db.cursor() as cursor:
            cursor.execute("""
                INSERT INTO sellers(
                    seller_category_id,
                    account,
                    password,
                    seller_name_ko,
                    seller_name_en,
                    cs_contact,
                    is_master,
                    is_delete
                )
                VALUES (
                    %(seller_category_id)s,
                    %(account)s,
                    %(password)s,
                    %(seller_name_ko)s,
                    %(seller_name_en)s,
                    %(cs_contact)s,
                    %(is_master)s,
                    False
                )
            """, data)

            return cursor.lastrowid

    def sign_in(self, db, data):
        """
        유저 로그인
        :param db: db_connection
        :param data: request body
        :return: 유저정보 (id)
        """

        with db.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    id,
                    account,
                    password
                FROM 
                    sellers
                WHERE
                    account = %(account)s
            """, data)

            return cursor.fetchone()

    def seller_category_type(self, db):
        """
        회원가입 시 셀러 카테고리 정보 가져오기
        :param db: db_connection
        :return: 셀러 카테고리 리스트
        """
        
        with db.cursor() as cursor:
            cursor.execute("""
                SELECT
                    id,
                    name
                FROM 
                    seller_categories_type
            """)

            return cursor.fetchall()

    def get_seller_list(self, db, filters):
        """
        셀러 회원 목록 가져오기
        :param filters: 회원 목록 필터
        :param db: db_connection
        :return: 셀러 회원 목록
        """
        
        with db.cursor() as cursor:
            sql = """
                SELECT
                    info.id,
                    seller.account,
                    seller.seller_name_en AS name_en,
                    seller.seller_name_ko AS name_ko,
                    manager.manager_name,
                    manager.manager_mobile,
                    manager.manager_email,
                    category.name AS category,
                    date_format(info.created_at, "%%Y-%%m-%%d %%T") AS created_at
                FROM
                    sellers_informations AS info
                INNER JOIN
                    sellers AS seller ON info.seller_id = seller.id
                INNER JOIN
                    seller_categories_type AS category ON seller.seller_category_id = category.id
                INNER JOIN
                    shop_status_type AS shop ON info.shop_status_id = shop.id
                LEFT JOIN
                    managers AS manager ON info.seller_id = manager.seller_id
                WHERE
                    info.is_delete = False
                """

            if 'id' in filters:
                sql += ' AND info.id = %(id)s'
            if 'account' in filters:
                sql += ' AND seller.account = %(account)s'
            if 'name_en' in filters:
                sql += ' AND seller.seller_name_en = %(name_en)s'
            if 'name_ko' in filters:
                sql += ' AND seller.seller_name_ko = %(name_ko)s'
            if 'manager_name' in filters:
                sql += ' AND manager.manager_name = %(manager_name)s'
            if 'manager_mobile' in filters:
                sql += ' AND manager.manger_mobile = %(manger_mobile)s'
            if 'manager_email' in filters:
                sql += ' AND manager.manager_email = %(manager_email)s'
            if 'category' in filters:
                sql += ' AND category.id = %(category)s'
            if 'start_date' in filters:
                sql += ' AND info.created_at >= %(start_date)s'
            if 'end_date' in filters:
                sql += '''
                AND info.created_at <= date_format(%(end_date)s, '%%Y-%%m-%%d 23:59:59')
                '''

            sql += ' GROUP BY info.id'
            cursor.execute(sql, filters)

            return cursor.rowcount, cursor.fetchall()

    def create_seller_information(self, db, seller_id):
        """
        셀러 상세정보 생성
        회원가입 시 기본값으로 생성
        :param db: db_connection
        :param seller_id: seller_id
        """

        with db.cursor() as cursor:
            cursor.execute("""
                INSERT INTO sellers_informations(
                    seller_id,
                    modifier_id,
                    shop_status_id
                ) 
                VALUES (
                    %s,
                    %s,                                        
                    1
                )
            """, (seller_id, seller_id))

    def get_seller_information(self, db, seller_id):
        """
        셀러 상세정보 가져오기
        :param db: db_connection
        :param seller_id: seller_id
        :return: 셀러 상세정보
        """

        with db.cursor() as cursor:
            cursor.execute("""
                SELECT
                    info.id,
                    info.seller_id,
                    info.shop_status_id,
                    info.profile_image,
                    info.short_introduction,
                    info.long_introduction,
                    info.background_image,
                    info.zipcode,
                    info.address,
                    date_format(info.cs_opening_time, "%%H:%%i") AS cs_opening_time,
                    date_format(info.cs_closing_time, "%%H:%%i") AS cs_closing_time,
                    info.delivery_information,
                    info.exchange_refund_information,
                    seller.account,
                    seller.seller_name_ko,
                    seller.seller_name_en,
                    seller.cs_contact,
                    status.name AS shop_status,
                    category.name AS category,
                    manager.manager_name,
                    manager.manager_mobile,
                    manager.manager_email
                FROM
                    sellers_informations AS info
                INNER JOIN
                    sellers AS seller ON info.seller_id = seller.id
                INNER JOIN
                    shop_status_type AS status ON info.shop_status_id = status.id
                INNER JOIN
                    seller_categories_type AS category ON seller.seller_category_id = category.id
                LEFT JOIN
                    managers AS manager ON info.seller_id = manager.seller_id
                WHERE
                    info.is_delete = False AND 
                    info.seller_id = %s
            """, seller_id)
            
            return cursor.fetchone()

    def update_seller_information(self, db, data):
        """
        셀러 상세정보 수정
        :param db: db_connection
        :param data: 셀러 상세정보
        """

        with db.cursor() as cursor:
            cursor.execute("""
                UPDATE
                    sellers_informations as info
                LEFT JOIN
                    sellers AS seller ON info.seller_id = seller.id
                SET
                    info.updated_at = NOW(),
                    info.profile_image = %(profile_image)s,
                    info.short_introduction = %(short_introduction)s,
                    info.long_introduction = %(long_introduction)s,
                    info.background_image = %(background_image)s,
                    info.zipcode = %(zipcode)s,
                    info.address = %(address)s,
                    info.cs_opening_time = %(cs_opening_time)s,
                    info.cs_closing_time = %(cs_closing_time)s,
                    info.delivery_information = %(delivery_information)s,
                    info.exchange_refund_information = %(exchange_refund_information)s,
                    info.modifier_id = %(modifier_id)s,
                    seller.seller_category_id = %(seller_category_id)s,
                    seller.cs_contact = %(cs_contact)s
                WHERE
                    info.seller_id = %(seller_id)s
            """, data)

    def update_shop_status(self, db, data):
        """
        셀러 상태(입점상태) 수정
        :param db: db_connection
        :param data: 셀러 상태
        """

        with db.cursor() as cursor:
            cursor.execute("""
                UPDATE
                    sellers_informations
                SET
                    shop_status_id = %(shop_status_id)s
                WHERE
                    seller_id = %(seller_id)s
            """, data)

    def create_managers(self, db, data):
        """
        담당 매니저 테이블 생성
        :param db: db_connection
        :param data: 매니저 정보
        """

        with db.cursor() as cursor:
            cursor.execute("""
                INSERT INTO managers(
                    seller_id,
                    manager_name,
                    manager_mobile,
                    manager_email,
                    modifier_id
                ) VALUES (
                    %(seller_id)s,
                    %(manager_name)s,
                    %(manager_mobile)s,
                    %(manager_email)s,
                    %(seller_id)s
                )
            """, data)

    def create_seller_logs(self, db, data):
        """
        셀러 로그 생성 (생성시, 수정시)
        :param db: db_connection
        :param data: 셀러 정보
        """

        with db.cursor() as cursor:
            cursor.execute("""
                INSERT INTO seller_logs(
                    seller_id,
                    shop_status_id,
                    account,
                    seller_name_ko,
                    seller_name_en,
                    cs_contact,
                    manager_name,
                    manager_mobile,
                    manager_email,
                    profile_image,
                    short_introduction,
                    long_introduction,
                    background_image,
                    zipcode,
                    address,
                    cs_opening_time,
                    cs_closing_time,
                    delivery_information,
                    exchange_refund_information
                ) VALUES(
                    %(seller_id)s,
                    %(shop_status_id)s,
                    %(account)s,
                    %(seller_name_ko)s,
                    %(seller_name_en)s,
                    %(cs_contact)s,
                    %(manager_name)s,
                    %(manager_mobile)s,
                    %(manager_email)s,
                    %(profile_image)s,
                    %(short_introduction)s,
                    %(long_introduction)s,
                    %(background_image)s,
                    %(zipcode)s,
                    %(address)s,
                    %(cs_opening_time)s,
                    %(cs_closing_time)s,
                    %(delivery_information)s,
                    %(exchange_refund_information)s
                )
            """, data)

    def get_seller_logs(self, db, seller_id):
        """
        가장 최근의 셀러 로그 정보 가져오기
        :param db: db_connection
        :param seller_id: seller_id
        :return: 최근 셀러 로그 정보
        """

        with db.cursor() as cursor:
            cursor.execute("""
                SELECT
                    seller_id,
                    shop_status_id,
                    account,
                    seller_name_ko,
                    seller_name_en,
                    cs_contact,
                    manager_name,
                    manager_mobile,
                    manager_email,
                    profile_image,
                    short_introduction,
                    long_introduction,
                    background_image,
                    zipcode,
                    address,
                    cs_opening_time,
                    cs_closing_time,
                    delivery_information,
                    exchange_refund_information
                FROM
                    seller_logs
                WHERE
                    seller_id = %s
                ORDER BY
                    id DESC LIMIT 1
            """, seller_id)

            return cursor.fetchone()
