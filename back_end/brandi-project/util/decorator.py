import jwt
import json
from functools import wraps

from flask import request, jsonify

from db_connection  import db_connection
from config         import SECRET, ALGORITHM
from model          import UserDao
from util.exception import JwtTokenException, NotExistsException


def login_decorator(func):
    """
    request 헤더에 있는 access_token 을 확인하여 로그인 유효성 체크
    토큰의 정보로 마스터여부 및 id값을 가져옵니다. (request.is_master, request.seller_id)
    토큰이 만료되었을때는 expired token 에러처리
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        db = None
        try:
            access_token = request.headers.get('Authorization', None)
            user_info    = jwt.decode(access_token, SECRET, algorithm=ALGORITHM)

            db = db_connection()
            seller = UserDao().check_account(db, user_info)

            if not seller:
                raise NotExistsException('not exists account', 400)

            if not seller['is_delete']:
                request.is_master = seller['is_master']
                request.seller_id = seller['id']
            else:
                raise JwtTokenException('invalid token', 401)

        except jwt.ExpiredSignatureError:
            return jsonify({'message' : 'expired token'}), 401
        except jwt.DecodeError:
            return jsonify({'message' : 'token decode error'}), 400
        finally:
            if db:
                db.close()
        return func(*args, **kwargs)
    return wrapper
