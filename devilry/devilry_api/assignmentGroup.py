from devilry.api_client.client import Client
from devilry.devilry_api.exceptions import NotValidRole
from devilry.settings import API_URL
from devilry.devilry_api.base import BaseAPi


class AssignmentGroup(BaseAPi):

    url = 'assignment-group/'
    query_params = ['ordering',
                    'search',
                    'period_short_name',
                    'subject_short_name',
                    'assignment_short_name',
                    'id',
                    'assignment_id']

    def __init__(self, key, action=None, role=None, **kwargs):
        # check role
        if role not in ['student', 'examiner']:
            raise NotValidRole()

        self.client = Client(API_URL)
        self.client.auth(key=key)
        self.role = role
        if action == 'list':
            self.list(**kwargs)

    def list(self, **kwargs):
        query_param = self.craft_queryparam(**kwargs)
        api = self.client.api('{}{}{}'.format(self.url, self.role, query_param))
        self.result = api.get()

    def pretty_print(self):
        print(self.result.json())

    def get_json(self):
        self.result.json()
