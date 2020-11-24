import jwt
import bcrypt
from datetime import datetime, timedelta

from model          import UserDao
from util.exception import NotExistsException, ExistsException, JwtTokenException
from config         import SECRET, ALGORITHM


class UserService:
    def __init__(self, user_dao):
        self.user_dao = user_dao

    def sign_up(self, db, data):
        """
        유저 회원가입
        이미 존재하는 아이디는 확인 후 예외처리,
        패스워드는 암호화하여 DB에 저장
        :param db: db_connection
        :param data: request body
        """

        if UserDao.check_account(self, db, data):
            raise ExistsException('already existed account', 409)

        hashed_pw = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        data['password'] = hashed_pw.decode('utf-8')

        UserDao.sign_up(self, db, data)

    def sign_in(self, db, data):
        """
        유저 로그인
        해당 유저가 존재하는지 체크하고 패스워드 일치 여부 확인,
        access_token과 refresh_token을 발급,
        refresh_token 기한 만료시에는 재발급
        :param db: db_connection
        :param data: request body
        :return: access_token, refresh_token
        """
        
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

        if UserDao.get_refresh_token(self, db, user_id):
            UserDao.update_refresh_token(self, db, token)
        else:
            UserDao.create_refresh_token(self, db, token)

        return {'access_token' : token['access_token'], 'refresh_token' : token['refresh_token']}

    def reissuance_token(self, db, data):
        """
        access_token 만료 시 토큰 재발급
        유저가 가지고있는 refresh_token과 비교하여 유효성, 기한만료 체크
        :param db: db_connection
        :param data: request body
        :return: access_token
        """

        user_id = UserDao.check_account(self, db, data)
        token = UserDao.get_refresh_token(self, db, user_id)

        if token['refresh_token'] != data['refresh_token']:
            raise JwtTokenException('invalid token', 401)
        elif token['expired_at'] < datetime.now():
            raise JwtTokenException('expired token', 401)

        user_info = data
        user_info['exp'] = datetime.now() + timedelta(seconds=30)
        access_token = jwt.encode(user_info, SECRET, algorithm=ALGORITHM).decode('utf-8')

        return access_token

    def seller_category_type(self, db):
        """
        셀러 카테고리 정보 가져오기
        :param db: db_connection
        :return: 카테고리 리스트
        """
        result = UserDao.seller_category_type(self, db)
        return result
