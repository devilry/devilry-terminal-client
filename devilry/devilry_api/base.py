import pprint
from devilry.devilry_api.exceptions import ResultIsNone


class BaseAPi(object):
    """
    Base api class contains useful utilities.
    """

    @property
    def url(self):
        """string: url string"""
        raise NotImplementedError('please implement url path for api Example: url = "assignment/"')

    @property
    def allowed_roles(self):
        """list: list of allowed roles"""
        raise NotImplementedError('please implement list of allowed roles'
                                  'Example: allowed_roles = ["exmainer", "student"]')

    @property
    def query_params(self):
        """list: list of allowed query parameters"""
        raise NotImplementedError('please implement query_params Example query_params = [\'search\', \'ordering\']')

    def check_role(self, role):
        """
        Check if the role passed is allowed

        Args:
            role: a role in string
        Raises:
            ValueError
        """
        if role not in self.allowed_roles:
            raise ValueError('role {} not allowed'.format(role))

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

    def parse_data(self, data):
        """
        Override this if you want to do something special with the data,
        for example parse datetime strings to objects.
        Args:
            data: data that should be parsed

        Returns:
            returns parsed data
        """
        return data

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
