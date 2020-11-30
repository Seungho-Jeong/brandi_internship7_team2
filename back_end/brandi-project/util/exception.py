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
