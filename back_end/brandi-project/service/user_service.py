import jwt
import bcrypt
import uuid
from datetime import datetime, timedelta

from util.exception import NotExistsException, ExistsException, InvalidValueException
from config         import SECRET, ALGORITHM, BUCKET_NAME


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
            raise ExistsException('이미 존재하는 계정입니다.', 409)

        hashed_pw = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        data['password'] = hashed_pw.decode('utf-8')

        seller_id = self.user_dao.sign_up(db, data)

        self.user_dao.create_seller_information(db, seller_id)
        data['manager_name'] = None
        data['manager_email'] = None
        data['ordering'] = 1
        data['seller_id'] = seller_id
        self.user_dao.create_managers(db, data)

        # 로그 테이블 생성
        user_info = self.user_dao.get_seller_information(db, seller_id)
        user_info['manager_name'] = None
        user_info['manager_mobile'] = data['manager_mobile']
        user_info['manager_email'] = None
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
            raise NotExistsException('아이디나 비밀번호가 일치하지 않습니다.', 400)

        user_info = self.user_dao.sign_in(db, data)

        if not bcrypt.checkpw(data['password'].encode('utf-8'), user_info['password'].encode('utf-8')):
            raise NotExistsException('아이디나 비밀번호가 일치하지 않습니다.', 400)

        exp = datetime.utcnow() + timedelta(days=1)
        access_token = jwt.encode({'account' : user_info['account'], 'exp' : exp}, SECRET, algorithm=ALGORITHM)

        return access_token.decode('utf-8')

    def seller_category_type(self, db):
        """
        셀러 카테고리 정보 가져오기
        :param db: db_connection
        :return: 카테고리 리스트
        """

        category = self.user_dao.seller_category_type(db)
        return category

    def get_seller_list(self, db, filters):
        """
        셀러 회원 목록 가져오기
        :param filters: 회원 목록 필터
        :param db: db_connection
        :return: 셀러 회원 목록
        """

        filters['limit'] = int(filters['limit']) if 'limit' in filters else 10
        filters['offset'] = (int(filters['offset']) - 1) * int(filters['limit']) if 'offset' in filters else 0

        count     = self.user_dao.get_seller_list_count(db, filters)
        user_info = self.user_dao.get_seller_list(db, filters)

        sellers = {
            'count'       : count['count'],
            'seller_list' : user_info
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
        managers  = self.user_dao.get_managers(db, seller_id)

        if not user_info:
            raise NotExistsException('존재하지 않는 셀러입니다.', 400)

        user_info['managers'] = managers

        return user_info

    def update_seller_information(self, db, data, s3, seller_id, modifier_id):
        """
        셀러 상세정보 수정
        담당매니저를 3개이상 등록하려고할 경우는 예외처리
        담당매니저 부분은 기존의 데이터와 비교해서 수정하거나 생성,삭제 처리
        :param s3: AWS S3 connection
        :param db: db_connection
        :param data: 셀러 상세정보
        :param modifier_id: modifier_id (수정자)
        :param seller_id: seller_id
        """

        manager_info = {}
        order_index = 1

        # 기존의 개수를 체크 -> ordering
        ordering = self.user_dao.get_ordering_managers(db, seller_id)
        exist_count = ordering['ordering']
        input_count = len(data['managers'])

        # 리스트를 3개 이상 요청했을 경우
        if len(data['managers']) > 3:
            raise InvalidValueException('담당매니저는 최대 3개까지만 등록할 수 있습니다.', 400)

        # 기존개수가 많으면 기존개수(exist_count)만큼, 기존개수가 더 적으면 입력개수(input_count)만큼 반복
        count = exist_count if exist_count > input_count else input_count

        for i in range(count):
            manager_info['seller_id'] = seller_id
            manager_info['ordering'] = order_index

            # 기존개수가 더 많을때 나머지는 삭제 (수정 -> 삭제)
            if (exist_count > input_count) and (i >= input_count):
                if order_index != 1:
                    self.user_dao.delete_managers(db, manager_info)
            else:
                # 기존 개수랑 같거나 + 기존이 더 적을때 일단 수정 그리고 생성
                manager_info['manager_name']   = data['managers'][i]['manager_name']
                manager_info['manager_email']  = data['managers'][i]['manager_email']
                manager_info['manager_mobile'] = data['managers'][i]['manager_mobile']

                if (exist_count < input_count) and (i >= exist_count):
                    # 수정 후 남은 개수만큼 생성 (수정 -> 생성)
                    self.user_dao.create_managers(db, manager_info)
                else:
                    # 개수가 같은 경우 (수정)
                    self.user_dao.update_managers(db, manager_info)

            order_index += 1

        data.pop('managers')
        data['seller_id'] = seller_id
        data['modifier_id'] = modifier_id

        # 파일 업로드
        if data['profile_image']:
            profile_image = data['profile_image']
            file_name = 'profile_' + str(uuid.uuid4())

            s3_path = f'image/user_image/{seller_id}/{file_name}'
            s3.put_object(
                Bucket=BUCKET_NAME,
                Body=profile_image,
                Key=s3_path,
                ContentType=profile_image.content_type)
            location = s3.get_bucket_location(Bucket=BUCKET_NAME)['LocationConstraint']
            image_url = f'https://{BUCKET_NAME}.s3.{location}.amazonaws.com/{s3_path}'
            data['profile_image'] = image_url

        if data['background_image']:
            background_image = data['background_image']
            file_name = 'background_' + str(uuid.uuid4())

            s3_path = f'image/user_image/{seller_id}/{file_name}'
            s3.put_object(
                Bucket=BUCKET_NAME,
                Body=background_image,
                Key=s3_path,
                ContentType=background_image.content_type)
            location = s3.get_bucket_location(Bucket=BUCKET_NAME)['LocationConstraint']
            image_url = f'https://{BUCKET_NAME}.s3.{location}.amazonaws.com/{s3_path}'
            data['background_image'] = image_url

        self.user_dao.update_seller_information(db, data)

        manager_info = self.user_dao.get_managers(db, seller_id)
        data['manager_name'] = manager_info[0]['manager_name'] if manager_info[0]['manager_name'] else None
        data['manager_mobile'] = manager_info[0]['manager_mobile']
        data['manager_email'] = manager_info[0]['manager_email'] if manager_info[0]['manager_email'] else None

        # 로그 생성
        user_log = self.user_dao.get_seller_logs(db, seller_id)
        for key in data:
            user_log[key] = data[key]

        self.user_dao.create_seller_logs(db, user_log)

    def update_shop_status(self, db, data, seller_id):
        """
        셀러 상태(입점상태) 수정
        존재하지않는 상태값(id)일 경우 not exists shop_status
        현재 상태에 맞지 않는 상태 값을 요청시 invalid shop_status_id
        :param db: db_connection
        :param data: 셀러 상태
        :param seller_id: seller_id
        """

        data['seller_id'] = seller_id
        shop_status_type = self.user_dao.check_shop_status(db, data['shop_status_id'])

        # 존재하지 않는 shop_status_id
        if not shop_status_type:
            raise NotExistsException('존재하지 않는 상태값(shop_status_id) 입니다.', 400)

        seller_status = self.user_dao.get_shop_status(db, seller_id)
        seller_status_id = seller_status['shop_status_id']

        # 현재 상태에 따른 상태 변경 exception
        if seller_status_id == 1:  # 입점대기
            if data['shop_status_id'] != 2:
                raise InvalidValueException('잘못된 상태값(shop_status_id) 입니다.', 400)

        elif seller_status_id == 2:  # 입점
            if data['shop_status_id'] != 4 and data['shop_status_id'] != 5:
                raise InvalidValueException('잘못된 상태값(shop_status_id) 입니다.', 400)

        elif seller_status_id == 3:  # 퇴점
            raise InvalidValueException('잘못된 상태값(shop_status_id) 입니다.', 400)

        elif seller_status_id == 4:  # 퇴점대기
            if data['shop_status_id'] != 2 and data['shop_status_id'] != 5 \
                    and data['shop_status_id'] != 3:
                raise InvalidValueException('잘못된 상태값(shop_status_id) 입니다.', 400)

        elif seller_status_id == 5:  # 휴점
            if data['shop_status_id'] != 2 and data['shop_status_id'] != 4:
                raise InvalidValueException('잘못된 상태값(shop_status_id) 입니다.', 400)

        self.user_dao.update_shop_status(db, data)
        
        # 로그 생성
        user_log = self.user_dao.get_seller_logs(db, seller_id)
        for key in data:
            user_log[key] = data[key]

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
        log_list.reverse()

        return log_list
