import jwt
import bcrypt
from datetime import datetime, timedelta

from model          import UserDao
from util.exception import NotExistsException, ExistsException, JwtTokenException
from config         import SECRET, ALGORITHM


class UserService:
    def sign_up(self, db, data):
        """
        유저 회원가입
        이미 존재하는 아이디는 확인 후 예외처리,
        패스워드는 암호화하여 DB에 저장
        :param db: db_connection
        :param data: request body
        """

        user_dao = UserDao()

        if user_dao.check_account(db, data):
            raise ExistsException('already existed account', 409)

        hashed_pw = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        data['password'] = hashed_pw.decode('utf-8')

        user_dao.sign_up(db, data)

        account = user_dao.check_account(db, data)
        if not data['is_master']:
            user_dao.create_seller_information(db, account)

    def sign_in(self, db, data):
        """
        유저 로그인
        해당 유저가 존재하는지 체크하고 패스워드 일치 여부 확인,
        access_token 만료 시에는 재발급
        :param db: db_connection
        :param data: request body
        :return: access_token, refresh_token
        """

        user_dao = UserDao()
        user_id = user_dao.check_account(db, data)

        if not user_id:
            raise NotExistsException('not exists account', 400)

        user_info = user_dao.sign_in(db, data)

        if not bcrypt.checkpw(data['password'].encode('utf-8'), user_info['password'].encode('utf-8')):
            raise NotExistsException('invalid account', 400)

        user_info['exp'] = datetime.now() + timedelta(seconds=30)
        access_token = jwt.encode(user_info, SECRET, algorithm=ALGORITHM).decode('utf-8')

        return access_token

    def reissuance_token(self, db, data):
        """
        access_token 만료 시 토큰 재발급
        :param db: db_connection
        :param data: request body
        :return: access_token
        """

        user_dao = UserDao()
        user_id = user_dao.check_account(db, data)
        token = user_dao.get_refresh_token(db, user_id)

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

        user_dao = UserDao()
        result = user_dao.seller_category_type(db)
        return result

    def get_seller_list(self, db, filters):
        """
        셀러 회원 목록 가져오기
        :param filters: 회원 목록 필터
        :param db: db_connection
        :return: 셀러 회원 목록
        """

        user_dao = UserDao()
        count = user_dao.get_seller_list_count(db, filters)
        seller_detail = user_dao.get_seller_list(db, filters)

        seller_list = [{
            'id'             : seller['id'],
            'account'        : seller['account'],
            'name_en'        : seller['name_en'],
            'name_ko'        : seller['name_ko'],
            'manager_name'   : seller['manager_name'],
            'manager_mobile' : seller['manager_mobile'],
            'manager_email'  : seller['manager_email'],
            'category'       : seller['category'],
            'created_at'     : seller['created_at']
        } for seller in seller_detail]

        sellers = {
            'count'       : count['count'],
            'seller_list' : seller_list
        }

        return sellers

    def get_seller_information(self, db, data):
        """
        셀러 상세정보 가져오기
        :param db: db_connection
        :param data: seller_id
        :return: 셀러 상세정보
        """

        user_dao = UserDao()
        result = user_dao.get_seller_information(db, data)

        if not result:
            raise NotExistsException('not exists seller', 400)

        return result

    def update_seller_information(self, db, data):
        user_dao = UserDao()
        user_dao.update_seller_information(db, data)

    def update_shop_status(self, db, data):
        user_dao = UserDao()
        user_dao.update_shop_status(db, data)
