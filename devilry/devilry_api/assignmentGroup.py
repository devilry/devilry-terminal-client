from devilry.api_client.client import Client
from devilry.devilry_api.exceptions import NotValidRole
from devilry.settings import API_URL
from devilry.devilry_api.base import BaseAPi
from devilry.devilry_api.feedbackset import Feedbackset


class AssignmentGroup(BaseAPi):
    """
    Wrapper class for the assignment group api

    Attributes:
        url (str): Url for assignment-group api.
        query_params (list): allowed query params.
        client (Client): client used to interact with api.
        role (str): This will be appended at the end of the ``self.url``
        key (str): api key
        result: response of the request will be stored here.
        feedback_sets (list): list of :obj:`Feedbackset`

    """

    url = 'assignment-group/'
    query_params = ['ordering',
                    'search',
                    'period_short_name',
                    'subject_short_name',
                    'assignment_short_name',
                    'id',
                    'assignment_id']

    def __init__(self, key, role, action=None, **kwargs):
        """
        initializes the class.

        Query parameters should be passed as kwargs.
        Query parameters supported: ordering, search, period_short_name,
                                    subject_short_name, assignment_short_name,
                                    id, assignment_id.
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
        self._feedback_sets = None
        if action == 'list':
            self.list(**kwargs)

    @property
    def feedback_sets(self):
        """
        Creates an instance of every related :class:`Feedbackset` in ``self.result``.

        Returns:
            list of :obj:`Feedbackset`
        """
        if self._feedback_sets is None:
            self._feedback_sets = []
            for assignment_group in self.get_json():
                self._feedback_sets.append(Feedbackset(self.key, self.role, group_id=assignment_group['id']))

        return self._feedback_sets

    def clear_feedback_sets(self):
        """
        Clears ``self._feedback_sets``.
        """
        self._feedback_sets = None

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
