

class NotValidRole(BaseException):

    def __str__(self):
        return repr('role not valid')