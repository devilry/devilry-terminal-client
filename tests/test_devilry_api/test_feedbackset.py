import unittest
import httpretty
import json
from datetime import datetime, timedelta
from sure import expect
from devilry.devilry_api import FeedbacksetList, Feedbackset
from devilry.api_client import Client
from helpers import mocks


class TestFeedbacksetList(unittest.TestCase):

    def setUp(self):
        self.client = Client('http://localhost:8000/api/')
        self.client.auth()

    def test_examiner_url(self):
        feedbackset = FeedbacksetList(self.client, 'examiner')
        self.assertEqual(feedbackset.get_url(), 'feedbackset/examiner')

    def test_student_url(self):
        feedbackset = FeedbacksetList(self.client, 'student')
        self.assertEqual(feedbackset.get_url(), 'feedbackset/student')

    @httpretty.activate
    def test_url_with_queryparams(self):
        feedbacksets = FeedbacksetList(
            self.client,
            'examiner',
            ordering='id',
            id=1,
            group_id=2
        )
        httpretty.register_uri(httpretty.GET, 'http://localhost:8000/api/feedbackset/examiner', body='[]')
        list = feedbacksets.feedbackset_list
        self.assertIsNone(list)
        expect(httpretty.last_request()).to.have.property("querystring").being.equal({
            'ordering': ['id'],
            'id': ['1'],
            'group_id': ['2']
        })

    @httpretty.activate
    def test_feedbackset_list(self):
        data = json.loads(mocks.feedbackset_list_mock_examiner_and_student)
        httpretty.register_uri(httpretty.GET, 'http://localhost:8000/api/feedbackset/examiner',
                               body=mocks.feedbackset_list_mock_examiner_and_student)
        feedbackset_list = FeedbacksetList(self.client, 'examiner')
        feedbacksets = feedbackset_list.feedbackset_list
        self.assertEqual(len(feedbacksets), 2)

        # First
        feedbackset1 = feedbacksets[0].data
        feedbackset1['deadline_datetime'] = feedbackset1['deadline_datetime'].isoformat()
        feedbackset1['created_datetime'] = feedbackset1['created_datetime'].isoformat()
        self.assertDictEqual(data[0], feedbackset1)

        # Second
        feedbackset2 = feedbacksets[1].data
        feedbackset2['deadline_datetime'] = feedbackset2['deadline_datetime'].isoformat()
        feedbackset2['created_datetime'] = feedbackset2['created_datetime'].isoformat()
        self.assertDictEqual(data[1], feedbackset2)


class TestFeedbackset(unittest.TestCase):

    def setUp(self):
        self.client = Client('http://localhost:8000/api/')
        self.client.auth()

    def test_examiner_url(self):
        feedbackset = Feedbackset(self.client, 'examiner', id=1)
        self.assertEqual(feedbackset.get_url(), 'feedbackset/examiner?id=1')

    def test_student_url(self):
        feedbackset = Feedbackset(self.client, 'student', id=1)
        self.assertEqual(feedbackset.get_url(), 'feedbackset/student?id=1')

    @httpretty.activate
    def test_url_queryparam(self):
        feedbackset = Feedbackset(self.client, 'student', id=1)

        # Mock api response
        httpretty.register_uri(httpretty.GET, 'http://localhost:8000/api/feedbackset/student',
                               body='[]')
        self.assertIsNone(feedbackset.data)
        expect(httpretty.last_request()).to.have.property("querystring").being.equal({
            'id': ['1']
        })

    def test_feedbackset_data_passed_url_and_data(self):
        data = json.loads(mocks.feedbackset_mock_examiner_and_student)[0]
        feedbackset = Feedbackset(self.client, 'examiner', data=data)
        self.assertEqual(feedbackset.get_url(), 'feedbackset/examiner?id={}'.format(data['id']))

        feedbackset1 = feedbackset.data
        feedbackset1['deadline_datetime'] = feedbackset1['deadline_datetime'].isoformat()
        feedbackset1['created_datetime'] = feedbackset1['created_datetime'].isoformat()
        self.assertDictEqual(data, feedbackset1)

    @httpretty.activate
    def test_feedbackset_data_fetched_by_id(self):
        data = json.loads(mocks.feedbackset_mock_examiner_and_student)[0]
        feedbackset = Feedbackset(self.client, 'student', id=data['id'])
        httpretty.register_uri(httpretty.GET, 'http://localhost:8000/api/feedbackset/student',
                               body=mocks.feedbackset_mock_examiner_and_student)
        feedbackset1 = feedbackset.data
        feedbackset1['deadline_datetime'] = feedbackset1['deadline_datetime'].isoformat()
        feedbackset1['created_datetime'] = feedbackset1['created_datetime'].isoformat()
        self.assertDictEqual(data, feedbackset1)

    @httpretty.activate
    def test_new_feedbackset(self):
        test_date_deadline = datetime.now() + timedelta(days=10)
        test_date_created = datetime.now()

        def request_callback(request, uri, headers):
            post_data = json.loads(json.loads(request.body.decode('utf-8')))
            response_data = json.loads(mocks.feedbackset_mock_examiner_and_student)[0]
            response_data['group_id'] = post_data['group_id']
            response_data['deadline_datetime'] = post_data['deadline_datetime']
            response_data['feedbackset_type'] = post_data['feedbackset_type']
            response_data['created_datetime'] = test_date_created.isoformat()
            return (201, headers, json.dumps(response_data))

        httpretty.register_uri(httpretty.POST, 'http://localhost:8000/api/feedbackset/examiner',
                               body=request_callback)

        feedbackset = Feedbackset.new(self.client, 'examiner', 1, test_date_deadline)
        self.assertEqual(feedbackset.data['deadline_datetime'], test_date_deadline)
        self.assertEqual(feedbackset.data['created_datetime'], test_date_created)
        self.assertEqual(feedbackset.data['group_id'], 1)

    @httpretty.activate
    def test_publish_feedbackset(self):
        data1 = json.loads(mocks.feedbackset_list_mock_examiner_and_student)[0]
        data2 = json.loads(mocks.feedbackset_list_mock_examiner_and_student)[1]

        httpretty.register_uri(httpretty.PATCH, 'http://localhost:8000/api/feedbackset/examiner',
                               body=json.dumps(data2))
        feedbackset = Feedbackset(self.client, 'examiner', data=data1)
        feedbackset.publish(2)
        expect(httpretty.last_request()).to.have.property("querystring").being.equal({
            'id': [str(data1['id'])],
            'grading_points': ['2']
        })
        feedbackset1 = feedbackset.data
        feedbackset1['deadline_datetime'] = feedbackset1['deadline_datetime'].isoformat()
        feedbackset1['created_datetime'] = feedbackset1['created_datetime'].isoformat()
        self.assertDictEqual(data2, feedbackset1)
