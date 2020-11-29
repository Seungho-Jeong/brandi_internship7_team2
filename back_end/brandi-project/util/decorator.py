import jwt
import json
from functools import wraps

from flask import request

from db_connection  import db_connection
from config         import SECRET, ALGORITHM
from model          import UserDao
from util.exception import JwtTokenException


def login_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        db = None
        try:
            access_token = request.headers.get('Authorization', None)
            user_info    = jwt.decode(access_token, SECRET, algorithm=ALGORITHM)

            db = db_connection()
            seller = UserDao().check_account(db, user_info)

            if not seller['is_delete']:
                request.is_master = seller['is_master']
                request.seller_id = seller['id']
            else:
                raise JwtTokenException('invalid token', 401)

        except jwt.ExpiredSignatureError:
            return json.dumps({'message' : 'expired token'}), 401
        except jwt.DecodeError:
            return json.dumps({'message' : 'token decode error'}), 400
        finally:
            if db:
                db.close()
        return func(*args, **kwargs)
    return wrapper
