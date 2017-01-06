import unittest
import httpretty
import json
from datetime import datetime, timedelta
from sure import expect
from devilry.devilry_api import GroupCommentList, GroupComment
from devilry.api_client import Client
from helpers import mocks


class TestGroupCommentList(unittest.TestCase):

    def setUp(self):
        self.client = Client('http://localhost:8000/api/')
        self.client.auth()

    def test_examiner_url(self):
        groupcomments = GroupCommentList(self.client, 'examiner', 5)
        self.assertEqual(groupcomments.get_url(), 'group-comment/examiner/5')

    def test_student_url(self):
        groupcomments = GroupCommentList(self.client, 'student', 5)
        self.assertEqual(groupcomments.get_url(), 'group-comment/student/5')

    @httpretty.activate
    def test_url_with_queryparams(self):
        groupcomments = GroupCommentList(
            self.client,
            'examiner',
            3,
            ordering='id',
            id=2
        )
        httpretty.register_uri(httpretty.GET, 'http://localhost:8000/api/group-comment/examiner/3', body='[]')
        list = groupcomments.group_comment_list
        self.assertIsNone(list)
        expect(httpretty.last_request()).to.have.property("querystring").being.equal({
            'ordering': ['id'],
            'id': ['2']
        })

    @httpretty.activate
    def test_group_comment_list(self):
        data = json.loads(mocks.group_comment_mock)
        httpretty.register_uri(httpretty.GET, 'http://localhost:8000/api/group-comment/student/2',
                               body=mocks.group_comment_mock)
        groupcomment_list = GroupCommentList(self.client, 'student', 2)
        groupcomments = groupcomment_list.group_comment_list
        self.assertEqual(len(groupcomments), 2)

        # First
        groupcomment1 = groupcomments[0].data
        groupcomment1['published_datetime'] = groupcomment1['published_datetime'].isoformat()
        groupcomment1['created_datetime'] = groupcomment1['created_datetime'].isoformat()
        self.assertDictEqual(data[0], groupcomment1)

        # Second
        groupcomment2 = groupcomments[1].data
        groupcomment2['published_datetime'] = groupcomment2['published_datetime'].isoformat()
        groupcomment2['created_datetime'] = groupcomment2['created_datetime'].isoformat()
        self.assertDictEqual(data[1], groupcomment2)


class TestGroupComment(unittest.TestCase):

    def setUp(self):
        self.client = Client('http://localhost:8000/api/')
        self.client.auth()

    def test_examiner_url(self):
        groupcomments = GroupComment(self.client, 'examiner', 5, id=2)
        self.assertEqual(groupcomments.get_url(), 'group-comment/examiner/5?id=2')

    def test_student_url(self):
        groupcomments = GroupComment(self.client, 'student', 5, id=7)
        self.assertEqual(groupcomments.get_url(), 'group-comment/student/5?id=7')

    @httpretty.activate
    def test_url_queryparam(self):
        groupcomment = GroupComment(
            self.client,
            'examiner',
            3,
            id=2
        )
        httpretty.register_uri(httpretty.GET, 'http://localhost:8000/api/group-comment/examiner/3', body='[]')
        data = groupcomment.data
        self.assertIsNone(data)
        expect(httpretty.last_request()).to.have.property("querystring").being.equal({
            'id': ['2']
        })

    def test_groupcomment_passed_url_and_data(self):
        data = json.loads(mocks.group_comment_mock)[0]
        groupcomment = GroupComment(self.client, 'student', 2, data=data)
        self.assertEqual(groupcomment.get_url(), 'group-comment/student/2?id={}'.format(data['id']))

        comment_data = groupcomment.data
        comment_data['published_datetime'] = comment_data['published_datetime'].isoformat()
        comment_data['created_datetime'] = comment_data['created_datetime'].isoformat()
        self.assertDictEqual(data, comment_data)

    @httpretty.activate
    def test_groupcomment_data_fetched_by_id(self):
        data = json.loads(mocks.group_comment_mock)[0]
        groupcomment = GroupComment(self.client, 'examiner', 2, id=data['id'])
        httpretty.register_uri(httpretty.GET, 'http://localhost:8000/api/group-comment/examiner/2',
                               body='[{}]'.format(json.dumps(data)))
        comment_data = groupcomment.data
        comment_data['published_datetime'] = comment_data['published_datetime'].isoformat()
        comment_data['created_datetime'] = comment_data['created_datetime'].isoformat()
        self.assertDictEqual(data, comment_data)

    @httpretty.activate
    def test_new_groupcomment(self):
        test_datetime = datetime.now()

        def request_callback(request, uri, headers):
            post_data = json.loads(json.loads(request.body.decode('utf-8')))
            response_data = json.loads(mocks.group_comment_mock)[0]
            response_data['published_datetime'] = test_datetime.isoformat()
            response_data['created_datetime'] = test_datetime.isoformat()
            response_data['text'] = post_data['text']
            response_data['part_of_grading'] = post_data['part_of_grading']
            return (201, headers, json.dumps(response_data))

        httpretty.register_uri(httpretty.POST, 'http://localhost:8000/api/group-comment/student/9',
                               body=request_callback)
        groupcomment = GroupComment.new(self.client, 'student', 9, 'coo man, coo!')
        self.assertEqual(groupcomment.data['published_datetime'], test_datetime)
        self.assertEqual(groupcomment.data['created_datetime'], test_datetime)
        self.assertFalse(groupcomment.data['part_of_grading'])
        self.assertEqual(groupcomment.data['text'], 'coo man, coo!')

    @httpretty.activate
    def test_delete_groupcomment(self):
        data = json.loads(mocks.group_comment_mock)[0]
        httpretty.register_uri(httpretty.DELETE,
                               'http://localhost:8000/api/group-comment/examiner/{}'.format(data['id']),
                               status=204)
        groupcomment = GroupComment(self.client, 'examiner', data['id'])
        groupcomment.delete()
