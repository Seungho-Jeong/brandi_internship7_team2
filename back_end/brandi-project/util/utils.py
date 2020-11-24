# import jwt
#
# from config import SECRET, ALGORITHM
# from model  import UserDao
#
# def check_token(func):
#     def wrapper(self, request, *args, **kwargs)
#         try:
#             access_token = request.headers.get('Authorization', None)
#             user_info = jwt.decode(access_token, SECRET, algorithm=ALGORITHM)
#             user = UserDao.check_account(UserDao, )
#
