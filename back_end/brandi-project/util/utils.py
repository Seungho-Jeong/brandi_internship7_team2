def check_account(cursor, data):
    cursor.execute("""
        SELECT
           account
        FROM sellers
        WHERE 
           account = %(account)s
    """, data)

    return cursor.fetchone()
