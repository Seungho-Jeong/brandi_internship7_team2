import jwt
import bcrypt
from datetime import datetime, timedelta

from model          import UserDao
from util.exception import NotExistsException, ExistsException
from config         import SECRET, ALGORITHM


class UserService:
    def __init__(self, user_dao):
        self.user_dao = user_dao

    def sign_up(self, db, data):
        if UserDao.check_account(self, db, data):
            raise ExistsException('already existed account', 409)

        hashed_pw = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        data['password'] = hashed_pw.decode('utf-8')

        UserDao.sign_up(self, db, data)

    def sign_in(self, db, data):
        user_id = UserDao.check_account(self, db, data)

        if not user_id:
            raise NotExistsException('not exists account', 400)

        user_info = UserDao.sign_in(self, db, data)

        if not bcrypt.checkpw(data['password'].encode('utf-8'), user_info['password'].encode('utf-8')):
            raise NotExistsException('invalid account', 400)

        time = datetime.now()
        user_info['exp'] = time + timedelta(seconds=30)
        access_token = jwt.encode(user_info, SECRET, algorithm=ALGORITHM).decode('utf-8')

        user_info['exp'] = time + timedelta(hours=1)
        refresh_token = jwt.encode(user_info, SECRET, algorithm=ALGORITHM).decode('utf-8')

        token = {
            'seller_id'     : user_id['id'],
            'access_token'  : access_token,
            'refresh_token' : refresh_token,
            'expired_at'    : time + timedelta(hours=1)
        }

        UserDao.create_refresh_token(self, db, token)

        return {'access_token' : token['access_token'], 'refresh_token' : token['refresh_token']}

    def reissuance_token(self, db, data):
        user_id = UserDao.check_account(self, db, data)
        token = UserDao.get_refresh_token(self, db, user_id)

        if token['refresh_token'] != data['refresh_token']:
            raise jwt.InvalidTokenError
        elif token['expired_at'] < datetime.now():
            raise jwt.ExpiredSignatureError

        user_info = data
        user_info['exp'] = datetime.now() + timedelta(seconds=30)
        access_token = jwt.encode(user_info, SECRET, algorithm=ALGORITHM).decode('utf-8')

        return access_token

    def seller_category_type(self, db):
        result = UserDao.seller_category_type(self, db)
        return result
