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
                    false
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

    def get_seller_list_count(self, db, filters):
        """
        셀러 회원 목록 개수 가져오기
        :param filters: 회원 목록 필터
        :param db: db_connection
        :return: 셀러 회원 목록 개수
        """

        with db.cursor() as cursor:
            sql = """
                SELECT
                    count(*) AS count
                FROM
                    sellers_informations AS info
                INNER JOIN
                    sellers AS seller ON info.seller_id = seller.id
                INNER JOIN
                    seller_categories_type AS category ON seller.seller_category_id = category.id
                INNER JOIN
                    shop_status_type AS shop ON info.shop_status_id = shop.id
                LEFT JOIN
                    managers AS m ON info.seller_id = m.seller_id AND m.ordering = 1
                WHERE
                    info.is_delete = false
                    AND seller.is_master = false
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
                sql += ' AND m.manager_name = %(manager_name)s'
            if 'manager_mobile' in filters:
                sql += ' AND m.manger_mobile = %(manger_mobile)s'
            if 'manager_email' in filters:
                sql += ' AND m.manager_email = %(manager_email)s'
            if 'category' in filters:
                sql += ' AND category.id = %(category)s'
            if 'start_date' in filters:
                sql += ' AND info.created_at >= %(start_date)s'
            if 'end_date' in filters:
                sql += '''
                AND info.created_at <= date_format(%(end_date)s, '%%Y-%%m-%%d 23:59:59')
                '''

            cursor.execute(sql, filters)

            return cursor.fetchone()

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
                    m.manager_name,
                    m.manager_mobile,
                    m.manager_email,
                    category.name AS category,
                    shop.id AS shop_status_id,
                    shop.name AS shop_status_name,
                    info.created_at
                FROM
                    sellers_informations AS info
                INNER JOIN
                    sellers AS seller ON info.seller_id = seller.id
                INNER JOIN
                    seller_categories_type AS category ON seller.seller_category_id = category.id
                INNER JOIN
                    shop_status_type AS shop ON info.shop_status_id = shop.id
                LEFT JOIN
                    managers AS m ON info.seller_id = m.seller_id AND m.ordering = 1
                WHERE
                    info.is_delete = false  
                    AND seller.is_master = false
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
                sql += ' AND m.manager_name = %(manager_name)s'
            if 'manager_mobile' in filters:
                sql += ' AND m.manger_mobile = %(manger_mobile)s'
            if 'manager_email' in filters:
                sql += ' AND m.manager_email = %(manager_email)s'
            if 'category' in filters:
                sql += ' AND category.id = %(category)s'
            if 'start_date' in filters:
                sql += ' AND info.created_at >= %(start_date)s'
            if 'end_date' in filters:
                sql += '''
                AND info.created_at <= date_format(%(end_date)s, '%%Y-%%m-%%d 23:59:59')
                '''

            sql += '''
                 ORDER BY info.id DESC
                 LIMIT %(limit)s
                 OFFSET %(offset)s
                '''

            cursor.execute(sql, filters)

            return cursor.fetchall()

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
                    info.modifier_id
                FROM
                    sellers_informations AS info
                INNER JOIN
                    sellers AS seller ON info.seller_id = seller.id
                INNER JOIN
                    shop_status_type AS status ON info.shop_status_id = status.id
                INNER JOIN
                    seller_categories_type AS category ON seller.seller_category_id = category.id
                WHERE
                    info.is_delete = false 
                    AND info.seller_id = %s
                LIMIT 1
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

    def check_shop_status(self, db, shop_status_id):
        """
        셀러 상태 유효 체크
        :param shop_status_id: shop_status_id
        :param db: db_connection
        :return: 셀러 상태 id
        """

        with db.cursor() as cursor:
            cursor.execute("""
                SELECT
                    id,
                    name
                FROM
                    shop_status_type
                WHERE
                    id = %s
            """, shop_status_id)

        return cursor.fetchone()

    def get_shop_status(self, db, seller_id):
        """
        해당 셀러 상태(입점상태) 조회
        :param db: db_connection
        :param seller_id: seller_id
        :return: 해당 셀러 상태(입점상태)
        """

        with db.cursor() as cursor:
            cursor.execute("""
                SELECT
                    shop_status_id
                FROM
                    sellers_informations
                WHERE
                    seller_id = %s
            """, seller_id)

        return cursor.fetchone()

    def update_shop_status(self, db, data):
        """
        해당 셀러 상태(입점상태) 수정
        :param db: db_connection
        :param data: 해당 셀러 상태
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

    def get_ordering_managers(self, db, seller_id):
        """
        해당 셀러의 매니저 등록 정보 조회
        :param db: db_connection
        :param seller_id: seller_id
        :return:
        """

        with db.cursor() as cursor:
            cursor.execute("""
                SELECT
                    ordering
                FROM
                    managers
                WHERE
                    seller_id = %s
                ORDER BY
                    ordering DESC
                LIMIT 1
            """, seller_id)

            return cursor.fetchone()

    def get_managers(self, db, seller_id):
        """
        셀러 상세정보 담당 매니저 조회
        :param db: db_connection
        :param seller_id: seller_id
        :return: 담당 매니저 목록
        """

        with db.cursor() as cursor:
            cursor.execute("""
                SELECT
                    id AS manager_id,
                    manager_name,
                    manager_mobile,
                    manager_email
                FROM
                    managers
                WHERE
                    seller_id = %s
                ORDER BY
                    ordering ASC
                LIMIT 3
            """, seller_id)

            return cursor.fetchall()

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
                    modifier_id,
                    ordering
                ) VALUES (
                    %(seller_id)s,
                    %(manager_name)s,
                    %(manager_mobile)s,
                    %(manager_email)s,
                    %(seller_id)s,
                    %(ordering)s
                )
            """, data)

    def update_managers(self, db, data):
        """
        담당 매니저 정보 수정
        :param db: db_connection
        :param data: 매니저 정보
        """

        with db.cursor() as cursor:
            cursor.execute("""
                UPDATE
                    managers
                SET
                    manager_name = %(manager_name)s,
                    manager_mobile = %(manager_mobile)s,
                    manager_email = %(manager_email)s,
                    ordering = %(ordering)s
                WHERE
                    seller_id = %(seller_id)s
                    AND ordering = %(ordering)s
            """, data)

    def delete_managers(self, db, data):
        """
        담당 매니저 정보 삭제 처리
        :param db: db_connection
        :param data: seller_id, is_delete
        """

        with db.cursor() as cursor:
            cursor.execute("""
                DELETE FROM
                    managers
                WHERE
                    seller_id = %(seller_id)s
                    AND ordering = %(ordering)s
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
                    exchange_refund_information,
                    modifier_id
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
                    %(exchange_refund_information)s,
                    %(modifier_id)s
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
                    exchange_refund_information,
                    modifier_id
                FROM
                    seller_logs
                WHERE
                    seller_id = %s
                ORDER BY
                    id DESC 
                LIMIT 1
            """, seller_id)

            return cursor.fetchone()

    def get_seller_status_log(self, db, seller_id):
        """
        셀러 상세 히스토리 정보 조회
        :param db: db_connection
        :param seller_id: seller_id
        :return: 상세 히스토리 리스트(시간, 입점상태, 수정자)
        """

        with db.cursor() as cursor:
            cursor.execute("""
                SELECT
                    log.id,
                    log.created_at,
                    shop.name AS shop_status,
                    seller.account AS modifier,
                    @rownum := @rownum + 1 AS no
                FROM
                    (select @rownum := 0) AS rownum,
                    seller_logs AS log
                INNER JOIN 
                    sellers AS seller ON log.modifier_id = seller.id
                INNER JOIN
                    shop_status_type AS shop on log.shop_status_id = shop.id
                WHERE
                    log.seller_id = %s
                ORDER BY
                    log.id DESC 
            """, seller_id)

            return cursor.fetchall()
