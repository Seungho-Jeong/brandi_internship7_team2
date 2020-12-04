ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


class Errors(Exception):
    def __init__(self, message, status_code):
        self.message = 'error {}'.format(message)
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
    def __init__(self, message='permission denied', status_code=403):
        self.message = message
        self.status_code = status_code


class PathParameterException(Exception):
    def __init__(self, message, status_code=400):
        self.message = "required parameter '{}' is not present".format(message)
        self.status_code = status_code
