from util.exception import ExistsException, NotExistsException
from util           import utils


class UserDao:
    def sign_up(db, data):
        with db.cursor() as cursor:
            if utils.check_account(cursor, data):
                raise ExistsException('existed account')

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
                values(
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
        with db.cursor() as cursor:
            if not utils.check_account(cursor, data):
                raise NotExistsException('not existed account')

            cursor.execute("""
                SELECT 
                    account,
                    password
                FROM 
                    sellers
                WHERE
                    account = %(account)s
            """, data)

            result = cursor.fetchone()
            return result

    def seller_category_type(self, db):
        with db.cursor() as cursor:
            cursor.execute("""
                SELECT
                    id,
                    name
                FROM 
                    seller_categories_type
            """)

            result = cursor.fetchall()
            return result
