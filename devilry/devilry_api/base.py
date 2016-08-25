
class BaseAPi(object):

    def pretty_print(self):
        raise NotImplementedError('please implement pretty_print function')

    def get_json(self):
        raise NotImplementedError('please implement get_json function')
