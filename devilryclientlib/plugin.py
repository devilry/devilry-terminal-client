import json
from settings import API_URL


class BasePlugin(object):
    """
    This is a base plugin class.

    When creating a plugin subclass this class.
    It's important to set plugin equal to your new plugin class


    Examples:
        class Plugin(PluginBase):

            @classmethod
            def description(cls):
                return 'some description'

        plugin = Plugin

    """
    def run(self, args):
        raise NotImplementedError

    @classmethod
    def description(cls):
        raise NotImplementedError


class BaseApiPlugin(BasePlugin):
    """
    This is a base plugin class for api's


    Examples:
        class ApiPlugin(BaseApiPlugin):
           queryparams = ['search', 'ordering']

            @classmethod
            def description(cls):
                return 'this is a api for...'

        plugin = ApiPlugin
    """

    #: base url of the api
    url = API_URL

    #: list of query parameters
    #: Example: queryparams = ['ordering', 'id', 'search']
    queryparams = []

    def parse_queryparams(self, args):
        """
        Returns a string that will be passed into an url

        When using argparse the argument dest should be named as the query param the api expects.
        For example if the api expects '?search=something' dest in add_argument
        should be search.
        """
        arguments = vars(args)
        if hasattr(args, 'query_string') and arguments['query_string']:
            return arguments['query_string']
        if not self.queryparams:
            return ''
        query = ''
        for param in self.queryparams:
            if arguments[param]:
                query += '&{}={}'.format(param, arguments[param])
        if query:
            return '?{}'.format(query[1:])
        return ''

    def list_prettyprint(self, json_list):
        """
        Prettyprint json list
        """
        for item in json_list:
            print('\n')
            for key, value in item.items():
                print('{}: {}'.format(key, value))
