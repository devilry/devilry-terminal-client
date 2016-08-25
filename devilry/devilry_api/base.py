
class BaseAPi(object):

    @property
    def query_params(self):
        raise NotImplementedError('please implement query_params Example query_params = [\'search\', \'ordering\']')

    def pretty_print(self):
        raise NotImplementedError('please implement pretty_print function')

    def get_json(self):
        raise NotImplementedError('please implement get_json function')

    def craft_queryparam(self, **kwargs):
        q_param = ''
        for key, value in kwargs.items():
            if key in self.query_params:
                q_param += '&{}={}'.format(key, value)
        return '/?{}'.format(q_param[1:])
