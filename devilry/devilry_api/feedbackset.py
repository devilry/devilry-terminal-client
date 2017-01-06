from devilry.api_client.client import Client
from devilry.devilry_api.exceptions import NotValidRole
from devilry.settings import API_URL
from devilry.devilry_api.base import BaseAPi
from devilry.devilry_api.groupComment import GroupComment
import dateutil.parser
import json


class FeedbacksetList(BaseAPi):
    """
    List of feedbackset

    Attributes:
        url (str): Url for feedbackset api.
        query_params (list): allowed query params.
        client (Client): client used to interact with api.
        role (str): This will be appended at the end of the ``self.url``
        result: response of the request will be stored here.

    """

    url = 'feedbackset/'
    query_params = ['ordering',
                    'id',
                    'group_id']
    allowed_roles = ['student', 'examiner']

    def __init__(self, client, role, parent=None, **kwargs):
        """

        Args:
            client: :class:`~devilry.api_client.Client`
            role: student, examiner etc...
            parent: :class:`~devilry.devilry_api.AssignmentGroup`
            **kwargs: Arbitrary keyword arguments, query parameters should be passed as kwargs.
        """
        self.client = client
        self.check_role(role)
        self.role = role
        self.parent = parent
        self.result = None
        self._feedbackset_list = None
        self.query_param = self.craft_queryparam(**kwargs)

    @property
    def feedbackset_list(self):
        if self._feedbackset_list is None:
            api = self.client.api(self.get_url())
            self.result = api.get()
            json = self.get_json()
            if len(json) == 0:
                return None
            self._feedbackset_list = []
            for feedbackset in json:
                self._feedbackset_list.append(
                    Feedbackset(self.client, self.role, data=feedbackset, parent=self.parent))
        return self._feedbackset_list

    def refresh(self):
        """
        Refresh feedbackset list
        """
        self._feedbackset_list = None
        return self.feedbackset_list


class Feedbackset(BaseAPi):
    url = 'feedbackset/'
    query_params = ['id', 'grading_points']
    allowed_roles = ['student', 'examiner']

    def __init__(self, client, role, id=None, data=None, parent=None, **kwargs):
        """

        Args:
            client: :class:`~devilry.api_client.Client`
            role: student, examiner etc...
            id: id of Assignment group
            data: prefetched data
            parent: :class:`~devilry.devilry_api.AssignmentGroup`
            **kwargs:
        """
        # if not id and not data:
        #     raise ValueError('id and data cannot be None at same time!')
        self.client = client
        self.check_role(role)
        self.role = role
        self.result = None
        self._data = None
        self.parent = parent
        self.query_param = ''
        if data:
            self.query_param = self.craft_queryparam(id=data['id'])
            self._data = self.parse_data(data)
        elif id:
            self.query_param = self.craft_queryparam(id=id)

    @classmethod
    def new(cls, client, role, group_id, deadline_datetime, feedbackset_type='new_attempt'):
        """
        Creates a new feedbackset for assignment group with datetime and feedbackset_type

        Args:
            client: :class:`~devilry.api_client.Client`
            role: student, examiner etc...
            group_id: id of assignment group
            deadline_datetime: Datetime object
            feedbackset_type: new_attempt or re_edit

        Returns:
            :class:`devilry.devilry_api.Feedbackset`
        """
        feedbackset = Feedbackset(client, role)

        api = client.api(feedbackset.get_url())
        json_data = json.dumps({
            'group_id': group_id,
            'deadline_datetime': deadline_datetime.isoformat(),
            'feedbackset_type': feedbackset_type
        })
        feedbackset.result = api.post(json=json_data)
        data = feedbackset.get_json()
        feedbackset._data = feedbackset.parse_data(data)
        feedbackset.query_param = feedbackset.craft_queryparam(id=data['id'])
        return feedbackset

    def publish(self, grading_points):
        """
        Publishes a feedbackset with grading points
        Args:
            grading_points: grading points

        Returns:
            returns new data
        """
        temp = self.query_param
        self.query_param = self.craft_queryparam(id=self.data['id'], grading_points=grading_points)
        api = self.client.api(self.get_url())
        self.result = api.patch()
        json = self.get_json()
        self.query_param = temp
        self._data = self.parse_data(json)
        return self._data

    @property
    def data(self):
        """
        returns feedbackset data
        Returns:
            dictionary with feedbackset data
        """
        if self._data is None:
            api = self.client.api(self.get_url())
            self.result = api.get()
            json = self.get_json()
            if len(json) == 0:
                return None
            self._data = self.parse_data(json[0])
        return self._data

    def refresh(self):
        """
        Refresh data
        Returns:
            retyrbs dictionary with new data
        """
        self._data = None
        return self.data

    def parse_data(self, data):
        """
        Parse datetime strings to datetime objects
        Args:
            data: data to be parsed

        Returns:
            parsed data
        """
        parsed_data = data
        parsed_data['created_datetime'] = dateutil.parser.parse(parsed_data['created_datetime'])
        parsed_data['deadline_datetime'] = dateutil.parser.parse(parsed_data['deadline_datetime'])
        return parsed_data

# class Feedbackset(BaseAPi):
#     """
#     Wrapper class for the feedbackset api
#
#     Attributes:
#         url (str): Url for feedbackset api.
#         query_params (list): allowed query params.
#         client (Client): client used to interact with api.
#         role (str): This will be appended at the end of the ``self.url``
#         key (str): api key
#         result: response of the request will be stored here.
#         group_comments (list): list of :obj:`GroupComment`
#
#     """
#
#     url = 'feedbackset/'
#     query_params = ['ordering',
#                     'id',
#                     'group_id']
#
#     def __init__(self, key, role, action=None, **kwargs):
#         """
#         initializes the class.
#
#         Query parameters should be passed as kwargs.
#         Query parameters supported: ordering, id, group_id.
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
#         self._group_comments = None
#         if action == 'list':
#             self.list(**kwargs)
#         elif action == 'new':
#             self.new(**kwargs)
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
#
#     @property
#     def group_comments(self):
#         """
#         Creates an instance of every related :class:`GroupComment` in ``self.result``.
#
#         Returns:
#             list of :obj:`GroupComment`
#         """
#         if self._group_comments is None:
#             self._group_comments = []
#             for feedbackset in self.get_json():
#                 self._group_comments.append(GroupComment(self.key, self.role, feedbackset['id']))
#         return self._group_comments
#
#     def clear_group_comments(self):
#         """
#         Clears ``self._group_comments``.
#         """
#         self._group_comments = None
#
#     def new(self, **kwargs):
#         api = self.client.api('{}{}'.format(self.url, self.role))
#         self.result = api.post(**kwargs)
#
#     def get_json(self):
#         return self.result.json()
