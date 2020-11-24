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
                   id
                FROM 
                    sellers
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
                    False,
                    False
                )
            """, data)

    def sign_in(self, db, data):
        """
        유저 로그인
        :param db: db_connection
        :param data: request body
        :return: 유저정보 (아이디, 패스워드)
        """

        with db.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    account,
                    password
                FROM 
                    sellers
                WHERE
                    account = %(account)s
            """, data)

            return cursor.fetchone()

    def create_refresh_token(self, db, data):
        """
        리프레시 토큰 생성 시 DB에 저장
        :param db: db_connection
        :param data: request body
        """
        
        with db.cursor() as cursor:
            cursor.execute("""
                INSERT INTO seller_refresh_token(
                    seller_id,
                    refresh_token,
                    expired_at
                ) VALUES (
                    %(seller_id)s,
                    %(refresh_token)s,
                    %(expired_at)s
                )
            """, data)

    def get_refresh_token(self, db, data):
        """
        해당 계정에 대한 리프레시 토큰 가져오기
        :param db: db_connection
        :param data: request body
        :return: 리프레시 토큰 정보
        """

        with db.cursor() as cursor:
            cursor.execute("""
                SELECT
                    refresh_token,
                    expired_at
                FROM
                    seller_refresh_token
                WHERE
                    seller_id = %(id)s
            """, data)

            return cursor.fetchone()

    def update_refresh_token(self, db, data):
        """
        리프레시 토큰 만료시 해당 계정의 리프레시 토큰 업데이트(재발급)
        :param db: db_connection
        :param data: request body
        """

        with db.cursor() as cursor:
            cursor.execute("""
                UPDATE 
                    seller_refresh_token
                SET
                    refresh_token = %(refresh_token)s,
                    expired_at = %(expired_at)s
                WHERE
                    seller_id = %(seller_id)s
            """, data)

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
