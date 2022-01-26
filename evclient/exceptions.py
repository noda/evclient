class EVBadRequestException(Exception):
    def __init__(self, message='Bad Request'):
        self.message = message


class EVUnauthorizedException(Exception):
    def __init__(self, message='Unauthorized'):
        self.message = message


class EVRequestFailedException(Exception):
    def __init__(self, message='Request Failed'):
        self.message = message


class EVForbiddenException(Exception):
    def __init__(self, message='Forbidden'):
        self.message = message


class EVNotFoundException(Exception):
    def __init__(self, message='Not Found'):
        self.message = message


class EVConflictException(Exception):
    def __init__(self, message='Conflict'):
        self.message = message


class EVTooManyRequestsException(Exception):
    def __init__(self, message='Too Many Requests'):
        self.message = message


class EVInternalServerException(Exception):
    def __init__(self, message='Internal Server Error'):
        self.message = message


class EVFatalErrorException(Exception):
    def __init__(self, message='A fatal error occurred'):
        self.message = message
