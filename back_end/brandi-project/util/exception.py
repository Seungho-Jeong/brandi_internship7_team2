class ExistsException(Exception):
    def __init__(self, message):
        self.message = message


class NotExistsException(Exception):
    def __init__(self, message):
        self.message = message
