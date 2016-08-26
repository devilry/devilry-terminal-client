from requests import api

from devilry.api_client.exceptions import HTTP400, HTTP401, HTTP403, HTTP404, HTTP405, HTTP429, HTTP503


class Api(object):
    """
    This class is an Api instance.

    Examples:
        api = Api('http://example.com/api/list-things/')
        api.get()

        headers = {'Authorization': 'Token some_api_key'}
        api = Api('http://example.com/api/list-things/', headers=headers)
        api.get()
    """

    def __init__(self, url, headers=None, queryparams=None, **kwargs):
        self.url = url
        print(url)
        if queryparams:
            self.url += queryparams
        self.headers = headers or {}

    def handle_errors(self, status_code):
        """
        Handles common errors.

        """
        if status_code == 400:
            raise HTTP400
        if status_code == 401:
            raise HTTP401
        if status_code == 403:
            raise HTTP403
        if status_code == 404:
            raise HTTP404
        if status_code == 405:
            raise HTTP405
        if status_code == 529:
            raise HTTP429
        if status_code == 503:
            raise HTTP503

    def get(self, **kwargs):
        response = api.get(self.url, headers=self.headers, **kwargs)
        self.handle_errors(response.status_code)
        return response

    def post(self, **kwargs):
        response = api.post(self.url, headers=self.headers, **kwargs)
        self.handle_errors(response.status_code)
        return response

    def put(self, **kwargs):
        response = api.put(self.url, headers=self.headers, **kwargs)
        self.handle_errors(response.status_code)
        return response

    def patch(self, **kwargs):
        response = api.patch(self.url, headers=self.headers, **kwargs)
        self.handle_errors(response.status_code)
        return response
