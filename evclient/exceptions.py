class EVResponseError(Exception):
    def __init__(self, message='Unknown Error'):
        self.message = message

class EVBadRequestException(EVResponseError):
    def __init__(self, message='Bad Request'):
        self.message = message


class EVUnauthorizedException(EVResponseError):
    def __init__(self, message='Unauthorized'):
        self.message = message


class EVRequestFailedException(EVResponseError):
    def __init__(self, message='Request Failed'):
        self.message = message


class EVForbiddenException(EVResponseError):
    def __init__(self, message='Forbidden'):
        self.message = message


class EVNotFoundException(EVResponseError):
    def __init__(self, message='Not Found'):
        self.message = message


class EVConflictException(EVResponseError):
    def __init__(self, message='Conflict'):
        self.message = message


class EVTooManyRequestsException(EVResponseError):
    def __init__(self, message='Too Many Requests'):
        self.message = message


class EVInternalServerException(EVResponseError):
    def __init__(self, message='Internal Server Error'):
        self.message = message


class EVFatalErrorException(EVResponseError):
    def __init__(self, message='A fatal error occurred'):
        self.message = message

class EVUnexpectedStatusCodeException(EVResponseError):
    def __init__(self, message="Server returned an unexpected status code"):
        self.message = message
