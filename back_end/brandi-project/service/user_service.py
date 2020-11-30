import jwt
import bcrypt
from datetime import datetime, timedelta

from util.exception import NotExistsException, ExistsException
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
        :param data: 회원가입 정보
        """

        if self.user_dao.check_account(db, data):
            raise ExistsException('already existed account', 409)

        hashed_pw = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        data['password'] = hashed_pw.decode('utf-8')

        seller_id = self.user_dao.sign_up(db, data)

        self.user_dao.create_seller_information(db, seller_id)
        
        # 로그 테이블 생성
        user_info = self.user_dao.get_seller_information(db, seller_id)
        self.user_dao.create_seller_logs(db, user_info)

    def sign_in(self, db, data):
        """
        유저 로그인
        해당 유저가 존재하는지 체크하고 패스워드 일치 여부 확인,
        access_token 발급
        :param db: db_connection
        :param data: account(계정이름), password
        :return: access_token
        """

        user_id = self.user_dao.check_account(db, data)

        if not user_id:
            raise NotExistsException('not exists account', 400)

        user_info = self.user_dao.sign_in(db, data)

        if not bcrypt.checkpw(data['password'].encode('utf-8'), user_info['password'].encode('utf-8')):
            raise NotExistsException('invalid account', 400)

        exp = datetime.utcnow() + timedelta(minutes=30)
        access_token = jwt.encode({'account' : user_info['account'], 'exp' : exp}, SECRET, algorithm=ALGORITHM)

        return access_token.decode('utf-8')

    def seller_category_type(self, db):
        """
        셀러 카테고리 정보 가져오기
        :param db: db_connection
        :return: 카테고리 리스트
        """

        result = self.user_dao.seller_category_type(db)
        return result

    def get_seller_list(self, db, filters):
        """
        셀러 회원 목록 가져오기
        :param filters: 회원 목록 필터
        :param db: db_connection
        :return: 셀러 회원 목록
        """

        user_info = self.user_dao.get_seller_list(db, filters)
        
        offset = filters['offset'] if 'offset' in filters else 0
        limit  = filters['limit'] if 'limit' in filters else 10
        
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
        } for seller in user_info[1][offset:limit]]
        
        sellers = {
            'count'       : user_info[0],
            'seller_list' : seller_list
        }

        return sellers

    def get_seller_information(self, db, seller_id):
        """
        셀러 상세정보 가져오기
        :param db: db_connection
        :param seller_id: seller_id
        :return: 셀러 상세정보
        """

        user_info = self.user_dao.get_seller_information(db, seller_id)

        if not user_info:
            raise NotExistsException('not exists seller', 400)

        return user_info

    def update_seller_information(self, db, data, seller_id, modifier_id):
        """
        셀러 상세정보 수정
        :param db: db_connection
        :param data: 셀러 상세정보
        :param modifier_id: modifier_id (수정자)
        :param seller_id: seller_id
        """

        data['seller_id'] = seller_id
        data['modifier_id'] = modifier_id
        self.user_dao.update_seller_information(db, data)
        
        # 로그 생성
        user_log = self.user_dao.get_seller_logs(db, seller_id)
        for key in data:
            user_log[key] = data[key]

        self.user_dao.create_seller_logs(db, user_log)

    def update_shop_status(self, db, data, seller_id):
        """
        셀러 상태(입점상태) 수정
        :param db: db_connection
        :param data: 셀러 상태
        :param seller_id: seller_id
        """

        data['seller_id'] = seller_id
        self.user_dao.update_shop_status(db, data)
        
        # 로그 생성
        user_log = self.user_dao.get_seller_logs(db, seller_id)
        for key in data:
            user_log[key] = data[key]

        self.user_dao.create_seller_logs(db, user_log)

    def create_managers(self, db, data, seller_id):
        """
        담당 매니저 생성
        :param db: db_connection
        :param data: 매니저 정보
        :param seller_id: seller_id
        """

        data['seller_id'] = seller_id
        self.user_dao.create_managers(db, data)

        # 로그 생성
        user_log = self.user_dao.get_seller_logs(db, seller_id)
        user_log['manager_name'] = data['manager_name']
        user_log['manager_mobile'] = data['manager_mobile']
        user_log['manager_email'] = data['manager_email']

        self.user_dao.create_seller_logs(db, user_log)

    def get_seller_status_log(self, db, seller_id):
        """
        셀러 상세 히스토리 정보 조회
        :param db: db_connection
        :param seller_id: seller_id
        :return: 상세 히스토리 리스트(시간, 입점상태, 수정자)
        """

        user_log = self.user_dao.get_seller_status_log(db, seller_id)
        log_list = [{
            'no'          : int(log['no']),
            'created_at'  : log['created_at'],
            'shop_status' : log['shop_status'],
            'modifier'    : log['modifier']
        } for log in user_log]

        return log_list
