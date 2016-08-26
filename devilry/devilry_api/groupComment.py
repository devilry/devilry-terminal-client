from devilry.api_client.client import Client
from devilry.devilry_api.exceptions import NotValidRole
from devilry.settings import API_URL
from devilry.devilry_api.base import BaseAPi


class GroupComment(BaseAPi):
    """
    Wrapper class for the group comment api

    Attributes:
        url (str): Url for group comment api.
        query_params (list): allowed query params.
        client (Client): client used to interact with api.
        role (str): This will be appended at the end of the ``self.url``
        result: response of the request will be stored here.

    """

    url = 'group-comment/'
    query_params = ['ordering', 'id']

    def __init__(self, key, role, feedback_set, action=None, **kwargs):
        """
        initializes the class.

        Query parameters should be passed as kwargs.
        Query parameters supported: ordering, id.

        Args:
            key (str): the api key
            role (str): this could be student or examiner
            feedback_set (int): id of feedbackset
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
        if action == 'list':
            self.list(feedback_set, **kwargs)
        elif action == 'new':
            self.new(feedback_set, **kwargs)

    def list(self, feedbackset_id, **kwargs):
        """
        sends a get request with given query parameters to the api
        and stores the result in ``self.result``
        Args:
            **kwargs: Arbitrary keyword arguments.
        """
        query_param = self.craft_queryparam(**kwargs)
        api = self.client.api('{}{}/{}{}'.format(self.url, self.role, feedbackset_id, query_param))
        self.result = api.get()

    def new(self, feedbackset_id, text=None, **kwargs):
        """
        posts a comment to feedbackset_id
        and stores the result in ``self.result``
        Args:
            **kwargs: Arbitrary keyword arguments.

        Returns:
        """
        api = self.client.api('{}{}/{}'.format(self.url, self.role, feedbackset_id))
        self.result = api.post(data={'text': text})

