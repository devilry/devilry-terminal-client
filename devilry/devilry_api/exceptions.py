

class NotValidRole(BaseException):

    def __str__(self):
        return repr('role not valid')


class ResultIsNone(BaseException):

    def __str__(self):
        return repr('result cannot be None')