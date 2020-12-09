ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


class Errors(Exception):
    def __init__(self, message, status_code):
        self.message = message
        self.status_code = status_code


class ExistsException(Errors):
    pass


class NotExistsException(Errors):
    pass


class JwtTokenException(Errors):
    pass


class InvalidValueException(Errors):
    pass


class FileException(Errors):
    pass


class PermissionException(Exception):
    def __init__(self, message='권한이 없습니다.', status_code=403):
        self.message = message
        self.status_code = status_code


class PathParameterException(Exception):
    def __init__(self, message, status_code=400):
        self.message = f"파라미터 '{message}'이 필요합니다."
        self.status_code = status_code


class RequestException(Exception):
    def __init__(self, message='요청 값이 존재하지 않습니다.', status_code=400):
        self.message = message
        self.status_code = status_code