from devilry.api_client.client import Client
from devilry.devilry_api.exceptions import NotValidRole
from devilry.settings import API_URL
from devilry.devilry_api.base import BaseAPi
from devilry.devilry_api.assignmentGroup import AssignmentGroup


class Assignment(BaseAPi):
    """
    Wrapper class for the assignment api

    Attributes:
        url (str): Url for assignment api.
        query_params (list): allowed query params.
        client (Client): client used to interact with api.
        role (str): This will be appended at the end of the ``self.url``
        key (str): api key
        result: response of the request will be stored here.
        assignment_groups (list): list of :obj:`AssignmentGroup`

    """

    url = 'assignment/'
    query_params = ['ordering',
                    'search',
                    'period_short_name',
                    'subject_short_name',
                    'short_name',
                    'id']

    def __init__(self, key, role, action=None, **kwargs):
        """
        initializes the class.

        Query parameters should be passed as kwargs.
        Query parameters supported: ordering, search, period_short_name,
                                    subject_short_name, short_name, id.

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
        self.result = None
        self._assignment_groups = None
        if action == 'list':
            self.list(**kwargs)

    @property
    def assignment_groups(self):
        """
        Creates an instance of every related :class:`AssignmentGroup` in ``self.result``.

        Returns:
            list of :obj:`AssignmentGroup`
        """
        if self._assignment_groups is None:
            self._assignment_groups = []
            for assignmnet in self.get_json():
                self._assignment_groups.append(AssignmentGroup(self.key, self.role, assignmnet_id=assignmnet['id']))

        return self._assignment_groups

    def clear_assignment_groups(self):
        """
        Clears ``self._assignment_group``.
        """
        self._assignment_groups = None

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
