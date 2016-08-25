from devilry.api_client.client import Client
from devilry.devilry_api.exceptions import NotValidRole
from devilry.settings import API_URL
from devilry.devilry_api.base import BaseAPi


class Assignment(BaseAPi):

    url = '/assignment/'

    def __init__(self, key, action=None, role=None, **kwargs):
        # check role
        if role not in ['student', 'examiner']:
            raise NotValidRole()

        self.client = Client(API_URL)
        self.client.auth(key=key)
        if action == 'list':
            self.list(role=role, **kwargs)

    def list(self, role=None, **kwargs):
        api = self.client.api('{}{}'.format(self.url, role))
        self.result = api.get(**kwargs)

    def pretty_print(self):
        print(self.result.json())

    def get_json(self):
        self.result.json()