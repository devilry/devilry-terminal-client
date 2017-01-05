from devilry.api_client.client import Client
from devilry.devilry_api.exceptions import NotValidRole
from devilry.settings import API_URL
from devilry.devilry_api.base import BaseAPi
from devilry.devilry_api.assignmentGroup import AssignmentGroupList
import dateutil.parser


class AssignmentList(BaseAPi):
    """
    Contains list of :class:`~devilry.devilry_api.Assignment`

    Attributes:
        url (str): Url for assignment api.
        query_params (list): allowed query params.
        client (Client): client used to interact with api.
        role (str): This will be appended at the end of the ``self.url``
        result: response of the request will be stored here.
        assignment_list (list): list of :class:`~devilry.devilry_api.Assignment`
    """

    url = 'assignment/'

    query_params = ['ordering',
                    'search',
                    'period_short_name',
                    'subject_short_name',
                    'short_name',
                    'id']
    allowed_roles = ['student', 'examiner']

    def __init__(self, client, role, **kwargs):
        """
        Init Assignment List
        Args:
            client: :class:`~devilry.api_client.Client`
            role: student, examiner etc...
            **kwargs: Arbitrary keyword arguments, query parameters should be passed as kwargs.
        """
        self.client = client
        self.check_role(role)
        self.role = role
        self._assignment_list = None
        self.result = None
        self.query_param = self.craft_queryparam(**kwargs)

    @property
    def assignment_list(self):
        """
        Returns:
            List of :class:`devilry.devilry_api.Assignment`
        """
        if self._assignment_list is None:
            api = self.client.api(self.get_url())
            self.result = api.get()
            json = self.get_json()
            if len(json) == 0:
                return None
            self._assignment_list = []
            for assignment in json:
                self._assignment_list.append(Assignment(self.client, self.role, data=assignment))
        return self._assignment_list

    def refresh(self):
        """
        Refresh assignment list
        """
        self._assignment_list = None
        return self.assignment_list


class Assignment(BaseAPi):
    """
    Represents an Assignment

    Attributes:
        url (str): Url for assignment api.
        query_params (list): allowed query params.
        client (Client): client used to interact with api.
        role (str): This will be appended at the end of the ``self.url``
    """
    url = 'assignment/'
    query_params = ['id']
    allowed_roles = ['student', 'examiner']

    def __init__(self, client, role, id=None, data=None):
        """
        If json kwarg is passed we will just insert the json data into self.data.
        If id is passed we will ask the api for the given Assignment
        Args:
            client: :class:`~devilry.api_client.Client`
            role: student, examiner etc...
            id: id of Assignment
            data: prefetched data
        """
        if not id and not data:
            raise ValueError('id and data cannot be None at same time!')
        self.client = client
        self.check_role(role)
        self.role = role
        self._data = None
        self.result = None

        if data:
            self.query_param = self.craft_queryparam(id=data['id'])
            self._data = self.parse_data(data)
        elif id:
            self.query_param = self.craft_queryparam(id=id)

    def parse_data(self, data):
        """
        Parse data
        Args:
            data: data that should be parsed

        Returns:
            returns parsed data
        """
        parsed_data = data
        parsed_data['publishing_time'] = dateutil.parser.parse(parsed_data['publishing_time'])
        return parsed_data

    def refresh(self):
        """
        Refresh data
        Returns:
            returns dictionary with new data
        """
        self._data = None
        return self.data

    @property
    def data(self):
        """
        returns Assignment data
        Returns:
            dictionary with assignment data
        """
        if self._data is None:
            api = self.client.api(self.get_url())
            self.result = api.get()
            json = self.get_json()
            if len(json) == 0:
                return None
            self._data = self.parse_data(json[0])
        return self._data

    def assignment_group_list(self):
        """
        returns :class:`devilry.devilry_api.AssignmentGroupList` filtered on assignment_id
        Returns:
            :class:`devilry.devilry_api.AssignmentGroupList` object
        """
        return AssignmentGroupList(self.client, self.role, parent=self, assignment_id=self.data['id'])
# class Assignment(BaseAPi):
#     """
#     Wrapper class for the assignment api
#
#     Attributes:
#         url (str): Url for assignment api.
#         query_params (list): allowed query params.
#         client (Client): client used to interact with api.
#         role (str): This will be appended at the end of the ``self.url``
#         key (str): api key
#         result: response of the request will be stored here.
#         assignment_groups (list): list of :obj:`AssignmentGroup`
#
#     """
#
#     url = 'assignment/'
#     query_params = ['ordering',
#                     'search',
#                     'period_short_name',
#                     'subject_short_name',
#                     'short_name',
#                     'id']
#
#     def __init__(self, key, role, action=None, **kwargs):
#         """
#         initializes the class.
#
#         Query parameters should be passed as kwargs.
#         Query parameters supported: ordering, search, period_short_name,
#                                     subject_short_name, short_name, id.
#
#         Args:
#             key (str): the api key
#             role (str): this could be student or examiner
#             action [optional(str)]: action to execute
#             **kwargs: Arbitrary keyword arguments, query parameters should be passed as kwargs.
#
#         Raises:
#             NotValidRole
#         """
#         if role not in ['student', 'examiner']:
#             raise NotValidRole()
#
#         self.client = Client(API_URL)
#         self.client.auth(key=key)
#         self.role = role
#         self.key = key
#         self.result = None
#         self._assignment_groups = None
#         if action == 'list':
#             self.list(**kwargs)
#
#     @property
#     def assignment_groups(self):
#         """
#         Creates an instance of every related :class:`AssignmentGroup` in ``self.result``.
#
#         Returns:
#             list of :obj:`AssignmentGroup`
#         """
#         if self._assignment_groups is None:
#             self._assignment_groups = []
#             for assignmnet in self.get_json():
#                 self._assignment_groups.append(AssignmentGroup(self.key, self.role, assignmnet_id=assignmnet['id']))
#
#         return self._assignment_groups
#
#     def clear_assignment_groups(self):
#         """
#         Clears ``self._assignment_group``.
#         """
#         self._assignment_groups = None
#
#     def list(self, **kwargs):
#         """
#         sends a get request with given query parameters to the api
#         and stores the result in ``self.result``
#         Args:
#             **kwargs: Arbitrary keyword arguments.
#         """
#         query_param = self.craft_queryparam(**kwargs)
#         api = self.client.api('{}{}{}'.format(self.url, self.role, query_param))
#         self.result = api.get()
