from api_client.api import Api


class Client(object):
    """
    Creates a session

    Examples:
        client = Client('http://localhost:8000/api/')
        client.auth(key='61d4d0b047b4d753c29d1756a4a656045c7df521')
        api = client.api('student/assignment-list/')
        api.get()
    """

    def __init__(self, url):
        self.url = url

    def auth(self, key=None, user=None, password=None):
        """
        authenticates the session, this is important if the rest api
        requires authentication by api key or user/password

        """
        self.headers = {}
        if key:
            self.headers = {'Authorization': 'Token {}'.format(key)}

    def api(self, path):
        """
        Returns Api class for path

        Returns:
            :class:`~api_client.api.Api`
        """
        return Api('{}{}'.format(self.url, path), self.headers)
