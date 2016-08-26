from devilry.api_client.client import Client
from devilry.devilry_api.exceptions import NotValidRole
from devilry.settings import API_URL
from devilry.devilry_api.base import BaseAPi


class Feedbackset(BaseAPi):

    url = 'feedbackset/'
    query_params = ['ordering',
                    'id',
                    'group_id']

    def __init__(self, key, action=None, role=None, **kwargs):
        # check role
        if role not in ['student', 'examiner']:
            raise NotValidRole()

        self.client = Client(API_URL)
        self.client.auth(key=key)
        self.role = role
        if action == 'list':
            self.list(**kwargs)
        elif action == 'new':
            self.new(**kwargs)

    def list(self, **kwargs):
        query_param = self.craft_queryparam(**kwargs)
        api = self.client.api('{}{}{}'.format(self.url, self.role, query_param))
        self.result = api.get()

    def new(self, **kwargs):
        api = self.client.api('{}{}'.format(self.url, self.role))
        self.result = api.post(**kwargs)

    def get_json(self):
        return self.result.json()
