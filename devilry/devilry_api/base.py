import pprint
from devilry.devilry_api.exceptions import ResultIsNone


class BaseAPi(object):
    """
    Base api class contains useful utilities.
    """

    @property
    def url(self):
        raise NotImplementedError('please implement url path for api Example: url = "assignment/"')

    @property
    def allowed_roles(self):
        raise NotImplementedError('please implement list of allowed roles'
                                  'Example: allowed_roles = ["exmainer", "student"]')

    @property
    def query_params(self):
        """list: list of allowed query parameters"""
        raise NotImplementedError('please implement query_params Example query_params = [\'search\', \'ordering\']')

    def craft_queryparam(self, **kwargs):
        """
        craft query string for urls
        Args:
            **kwargs:

        Returns:
            query string

        """
        q_param = ''
        for key, value in kwargs.items():
            if key in self.query_params and value is not None:
                q_param += '&{}={}'.format(key, value)
        if q_param == '':
            return ''
        return '?{}'.format(q_param[1:])

    def pretty_print(self):
        if self.result is None:
            raise ResultIsNone()
        pprint.pprint(self.result.json())

    def get_json(self):
        if self.result is None:
            raise ResultIsNone()
        return self.result.json()

    def get_url(self):
        return '{}{}{}'.format(self.url, self.role, self.query_param)
