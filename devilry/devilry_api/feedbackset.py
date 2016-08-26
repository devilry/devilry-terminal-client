from devilry.api_client.client import Client
from devilry.devilry_api.exceptions import NotValidRole
from devilry.settings import API_URL
from devilry.devilry_api.base import BaseAPi
from devilry.devilry_api.groupComment import GroupComment


class Feedbackset(BaseAPi):
    """
    Wrapper class for the feedbackset api

    Attributes:
        url (str): Url for feedbackset api.
        query_params (list): allowed query params.
        client (Client): client used to interact with api.
        role (str): This will be appended at the end of the ``self.url``
        key (str): api key
        result: response of the request will be stored here.
        group_comments (list): list of :obj:`GroupComment`

    """

    url = 'feedbackset/'
    query_params = ['ordering',
                    'id',
                    'group_id']

    def __init__(self, key, role, action=None, **kwargs):
        """
        initializes the class.

        Query parameters should be passed as kwargs.
        Query parameters supported: ordering, id, group_id.

        Args:
            key (str): the api key
            role (str): this could be student or examiner
            action [optional(str)]: action to execute
            **kwargs: Arbitrary keyword arguments, query parameters should be passed as kwargs.

        Raises:
            NotValidRole
        """
        if role not in ['student', 'examiner']:
            raise NotValidRole()

        self.client = Client(API_URL)
        self.client.auth(key=key)
        self.role = role
        self.key = key
        self._group_comments = None
        if action == 'list':
            self.list(**kwargs)
        elif action == 'new':
            self.new(**kwargs)

    def list(self, **kwargs):
        """
        sends a get request with given query parameters to the api
        and stores the result in ``self.result``
        Args:
            **kwargs: Arbitrary keyword arguments.
        """
        query_param = self.craft_queryparam(**kwargs)
        api = self.client.api('{}{}{}'.format(self.url, self.role, query_param))
        self.result = api.get()

    @property
    def group_comments(self):
        """
        Creates an instance of every related :class:`GroupComment` in ``self.result``.

        Returns:
            list of :obj:`GroupComment`
        """
        if self._group_comments is None:
            self._group_comments = []
            for feedbackset in self.get_json():
                self._group_comments.append(GroupComment(self.key, self.role, feedbackset['id']))
        return self._group_comments

    def clear_group_comments(self):
        """
        Clears ``self._group_comments``.
        """
        self._group_comments = None

    def new(self, **kwargs):
        api = self.client.api('{}{}'.format(self.url, self.role))
        self.result = api.post(**kwargs)

    def get_json(self):
        return self.result.json()
