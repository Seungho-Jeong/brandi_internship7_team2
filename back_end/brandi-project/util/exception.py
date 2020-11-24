class ExistsException(Exception):
    def __init__(self, message, status_code):
        self.message = 'error {}'.format(message)
        self.status_code = status_code


class NotExistsException(Exception):
    def __init__(self, message, status_code):
        self.message = 'error {}'.format(message)
        self.status_code = status_code


class JwtTokenException(Exception):
    def __init__(self, message, status_code):
        self.message = 'error {}'.format(message)
        self.status_code = status_code
