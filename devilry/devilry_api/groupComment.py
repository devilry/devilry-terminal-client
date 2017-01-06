from devilry.api_client.client import Client
from devilry.devilry_api.exceptions import NotValidRole
from devilry.settings import API_URL
from devilry.devilry_api.base import BaseAPi
import dateutil.parser
import json


class GroupCommentList(BaseAPi):
    """
    List of group comments

    Attributes:
        url (str): Url for group comment api.
        query_params (list): allowed query params.
        client (Client): client used to interact with api.
        role (str): This will be appended at the end of the ``self.url``
        result: response of the request will be stored here.

    """
    url = 'group-comment/'
    query_params = ['ordering', 'id']
    allowed_roles = ['student', 'examiner']

    def __init__(self, client, role, feedback_set, parent=None, **kwargs):
        """
        initializes the class.

        Query parameters should be passed as kwargs.
        Query parameters supported: ordering, id.

        Args:
            client: :class:`~devilry.api_client.Client`
            role (str): this could be student or examiner
            feedback_set (int): id of feedbackset
            parent: class:`~devilry.devilry_api.Feedbackset`
            **kwargs: Arbitrary keyword arguments, query parameters should be passed as kwargs.

        Raises:
            NotValidRole
        """
        self.client = client
        self.check_role(role)
        self.role = role
        self.parent = parent
        self.result = None
        self._group_comment_list = None
        self.query_param = self.craft_queryparam(**kwargs)
        self.path_param = feedback_set

    @property
    def group_comment_list(self):
        if self._group_comment_list is None:
            api = self.client.api(self.get_url())
            self.result = api.get()
            json = self.get_json()
            if len(json) == 0:
                return None
            self._group_comment_list = []
            for comment in json:
                self._group_comment_list.append(
                    GroupComment(self.client, self.role, self.path_param, data=comment, parent=self.parent))
        return self._group_comment_list

    def refresh(self):
        """
        Refresh group comment list
        """
        self._group_comment_list = None
        return self.group_comment_list


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
    query_params = ['id']
    allowed_roles = ['student', 'examiner']

    def __init__(self, client, role, feedback_set, id=None, data=None, parent=None, **kwargs):
        """

        Args:
            client: :class:`~devilry.api_client.Client`
            role (str): this could be student or examiner
            feedback_set (int): id of feedbackset
            id (int): id of feedbackset
            data (dict): data
            parent: class:`~devilry.devilry_api.Feedbackset`
            **kwargs:
        """
        self.client = client
        self.check_role(role)
        self.role = role
        self.result = None
        self._data = None
        self.parent = parent
        self.query_param = ''
        self.path_param = feedback_set

        if data:
            self.query_param = self.craft_queryparam(id=data['id'])
            self._data = self.parse_data(data)
        elif id:
            self.query_param = self.craft_queryparam(id=id)

    @classmethod
    def new(cls, client, role, feedback_set, text, part_of_grading=False):
        """
        Creates a new comment on feedbackset
        Args:
            client: :class:`~devilry.api_client.Client`
            role: student, examiner etc...
            feedback_set: id of feedbackset to post comment on
            text: comment text
            part_of_grading: tru or false

        Returns:
            :class:`~devilry.devilry_api.GroupComment`
        """
        groupcomment = GroupComment(client, role, feedback_set)

        api = client.api(groupcomment.get_url())
        json_data = json.dumps({
            'text': text,
            'part_of_grading': part_of_grading
        })
        groupcomment.result = api.post(json=json_data)
        data = groupcomment.get_json()
        groupcomment._data = groupcomment.parse_data(data)
        groupcomment.query_param = groupcomment.craft_queryparam(id=data['id'])
        return groupcomment

    def delete(self):
        """
        Delete comment
        """
        api = self.client.api(self.get_url())
        self.result = api.delete()

    @property
    def data(self):
        """
        returns group comment data
        Returns:
            dictionary with group comment data
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
            returns dictionary with new data
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
        parsed_data['published_datetime'] = dateutil.parser.parse(parsed_data['published_datetime'])
        parsed_data['created_datetime'] = dateutil.parser.parse(parsed_data['created_datetime'])
        return parsed_data

# class GroupComment(BaseAPi):
#     """
#     Wrapper class for the group comment api
#
#     Attributes:
#         url (str): Url for group comment api.
#         query_params (list): allowed query params.
#         client (Client): client used to interact with api.
#         role (str): This will be appended at the end of the ``self.url``
#         result: response of the request will be stored here.
#
#     """
#
#     url = 'group-comment/'
#     query_params = ['id']
#
#     def __init__(self, key, role, feedback_set, action=None, **kwargs):
#         """
#         initializes the class.
#
#         Query parameters should be passed as kwargs.
#         Query parameters supported: ordering, id.
#
#         Args:
#             key (str): the api key
#             role (str): this could be student or examiner
#             feedback_set (int): id of feedbackset
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
#         if action == 'list':
#             self.list(feedback_set, **kwargs)
#         elif action == 'new':
#             self.new(feedback_set, **kwargs)
#
#     def list(self, feedbackset_id, **kwargs):
#         """
#         sends a get request with given query parameters to the api
#         and stores the result in ``self.result``
#         Args:
#             **kwargs: Arbitrary keyword arguments.
#         """
#         query_param = self.craft_queryparam(**kwargs)
#         api = self.client.api('{}{}/{}{}'.format(self.url, self.role, feedbackset_id, query_param))
#         self.result = api.get()
#
#     def new(self, feedbackset_id, text=None, **kwargs):
#         """
#         posts a comment to feedbackset_id
#         and stores the result in ``self.result``
#         Args:
#             **kwargs: Arbitrary keyword arguments.
#
#         Returns:
#         """
#         api = self.client.api('{}{}/{}'.format(self.url, self.role, feedbackset_id))
#         self.result = api.post(data={'text': text})

