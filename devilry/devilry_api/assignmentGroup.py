from devilry.api_client.client import Client
from devilry.devilry_api.exceptions import NotValidRole
from devilry.settings import API_URL
from devilry.devilry_api.base import BaseAPi
from devilry.devilry_api.feedbackset import Feedbackset, FeedbacksetList


class AssignmentGroupList(BaseAPi):
    """
    Wrapper class for the assignment group api

    Attributes:
        url (str): Url for assignment-group api.
        query_params (list): allowed query params.
        client (Client): client used to interact with api.
        role (str): This will be appended at the end of the ``self.url``
        result: response of the request will be stored here.
        assignment_group_list (list): list of :class:`~devilry.devilry_api.AssignmentGroup`

    """

    url = 'assignment-group/'
    query_params = ['ordering',
                    'search',
                    'period_short_name',
                    'subject_short_name',
                    'assignment_short_name',
                    'id',
                    'assignment_id']
    allowed_roles = ['student', 'examiner']

    def __init__(self, client, role, parent=None, **kwargs):
        """
        Init Assignment gorup List
        Args:
            client: :class:`~devilry.api_client.Client`
            role: student, examiner etc...
            parent: :class:`~devilry.devilry_api.Assignment`
            **kwargs: Arbitrary keyword arguments, query parameters should be passed as kwargs.
        """
        self.client = client
        self.check_role(role)
        self.role = role
        self.parent = parent
        self.result = None
        self._assignment_group_list = None
        self.query_param = self.craft_queryparam(**kwargs)

    @property
    def assignment_group_list(self):
        """
        Returns:
            List of :class:`~devilry.devilry_api.AssignmentGroup`
        """
        if self._assignment_group_list is None:
            api = self.client.api(self.get_url())
            self.result = api.get()
            json = self.get_json()
            if len(json) == 0:
                return None
            self._assignment_group_list = []
            for group in json:
                self._assignment_group_list.append(
                    AssignmentGroup(self.client, self.role, data=group, parent=self.parent))
        return self._assignment_group_list

    def refresh(self):
        """
        Refresh assignment group list
        """
        self._assignment_group_list = None
        return self.assignment_group_list


class AssignmentGroup(BaseAPi):
    """
    Represents an AssignmentGroup
    Attributes:
        url (str): Url for assignment api.
        query_params (list): allowed query params.
        client (Client): client used to interact with api.
        role (str): This will be appended at the end of the ``self.url``
    """

    url = 'assignment-group/'
    query_params = ['id']
    allowed_roles = ['student', 'examiner']

    def __init__(self, client, role, id=None, data=None, parent=None, **kwargs):
        """
        If json kwarg is passed we will just insert the json data into self.data.
        If id is passed we will ask the api for the given AssignmentGroup.
        Args:
            client: :class:`~devilry.api_client.Client`
            role: student, examiner etc...
            id: id of Assignment group
            data: prefetched data
            parent: :class:`~devilry.devilry_api.Assignment`
            **kwargs:
        """
        if not id and not data:
            raise ValueError('id and data cannot be None at same time!')
        self.client = client
        self.check_role(role)
        self.role = role
        self.result = None
        self._data = None
        self.parent = parent

        if data:
            self.query_param = self.craft_queryparam(id=data['id'])
            self._data = self.parse_data(data)
        elif id:
            self.query_param = self.craft_queryparam(id=id)

    @property
    def data(self):
        """
        returns Assignment group data.
        Returns:
            dictionary with assignment group data
        """
        if self._data is None:
            api = self.client.api(self.get_url())
            self.result = api.get()
            json = self.get_json()
            if len(json) == 0:
                return None
            self._data = self.parse_data(json[0])
        return self._data

    def feedbackset_list(self):
        """
        Returns :class:`~devilry.devilry_api.FeedbacksetList` filtered on group_id
        Returns:
            :class:`devilry.devilry_api.FeedcbaksetList` object
        """
        return FeedbacksetList(self.client, self.role, parent=self, group_id=self.data['id'])

# class AssignmentGroup(BaseAPi):
#     """
#     Wrapper class for the assignment group api
#
#     Attributes:
#         url (str): Url for assignment-group api.
#         query_params (list): allowed query params.
#         client (Client): client used to interact with api.
#         role (str): This will be appended at the end of the ``self.url``
#         key (str): api key
#         result: response of the request will be stored here.
#         feedback_sets (list): list of :obj:`Feedbackset`
#
#     """
#
#     url = 'assignment-group/'
#     query_params = ['ordering',
#                     'search',
#                     'period_short_name',
#                     'subject_short_name',
#                     'assignment_short_name',
#                     'id',
#                     'assignment_id']
#
#     def __init__(self, key, role, action=None, **kwargs):
#         """
#         initializes the class.
#
#         Query parameters should be passed as kwargs.
#         Query parameters supported: ordering, search, period_short_name,
#                                     subject_short_name, assignment_short_name,
#                                     id, assignment_id.
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
#         self._feedback_sets = None
#         if action == 'list':
#             self.list(**kwargs)
#
#     @property
#     def feedback_sets(self):
#         """
#         Creates an instance of every related :class:`Feedbackset` in ``self.result``.
#
#         Returns:
#             list of :obj:`Feedbackset`
#         """
#         if self._feedback_sets is None:
#             self._feedback_sets = []
#             for assignment_group in self.get_json():
#                 self._feedback_sets.append(Feedbackset(self.key, self.role, group_id=assignment_group['id']))
#
#         return self._feedback_sets
#
#     def clear_feedback_sets(self):
#         """
#         Clears ``self._feedback_sets``.
#         """
#         self._feedback_sets = None
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
