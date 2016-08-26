from devilry.api_client.client import Client
from devilry.devilry_api.exceptions import NotValidRole
from devilry.settings import API_URL
from devilry.devilry_api.base import BaseAPi


class GroupComment(BaseAPi):

    url = 'group-comment'
    query_params = ['ordering', 'id']

    def __init__(self, key, feedback_set, action=None, role=None, **kwargs):
        # check role
        if role not in ['student', 'examiner']:
            raise NotValidRole()

        self.client = Client(API_URL)
        self.client.auth(key=key)
        self.role = role
        if action == 'list':
            self.list(feedback_set, **kwargs)
        elif action == 'new':
            self.new(**kwargs)

    def list(self, feedbackset_id, **kwargs):
        query_param = self.craft_queryparam(**kwargs)
        api = self.client.api('{}/{}/{}{}'.format(self.url, self.role, feedbackset_id, query_param))
        self.result = api.get()
