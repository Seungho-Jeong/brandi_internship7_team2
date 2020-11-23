import jwt
import bcrypt
from datetime import datetime, timedelta

from model          import UserDao
from util.exception import NotExistsException
from config         import SECRET, ALGORITHM


class UserService:
    def __init__(self, user_dao):
        self.user_dao = user_dao

    def sign_up(db, data):
        hashed_pw = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        data['password'] = hashed_pw.decode('utf-8')

        UserDao.sign_up(db, data)

    def sign_in(self, db, data):
        user_info = UserDao.sign_in(db, data)

        if not bcrypt.checkpw(data['password'].encode('utf-8'), user_info['password'].encode('utf-8')):
            raise NotExistsException('invalid account')

        user_info['exp'] = datetime.utcnow() + timedelta(seconds=30)
        access_token = jwt.encode(user_info, SECRET, algorithm=ALGORITHM)
        return access_token.decode('utf-8')

    def seller_category_type(self, db):
        result = UserDao.seller_category_type(UserDao(), db)
        return result
