import unittest
import httpretty
import json
from sure import expect
from devilry.devilry_api import AssignmentList, Assignment
from devilry.api_client import Client
from helpers import mocks


class TestAssignmentList(unittest.TestCase):

    def setUp(self):
        self.client = Client('http://localhost:8000/api/')
        self.client.auth()

    def test_examiner_url(self):
        assignment_list = AssignmentList(client=self.client, role='examiner')
        self.assertEqual(assignment_list.get_url(), 'assignment/examiner')

    def test_student_url(self):
        assignment_list = AssignmentList(client=self.client, role='student')
        self.assertEqual(assignment_list.get_url(), 'assignment/student')

    @httpretty.activate
    def test_examiner_url_with_queryparams(self):
        assignment_list = AssignmentList(
            client=self.client,
            role='examiner',
            ordering='short_name',
            search='cool',
            period_short_name='spriing',
            subject_short_name='duck1010',
            short_name='superCool',
            id='1'
        )
        httpretty.register_uri(httpretty.GET, 'http://localhost:8000/api/assignment/examiner', body='[]')
        list = assignment_list.assignment_list
        self.assertEqual(list, None)
        expect(httpretty.last_request()).to.have.property("querystring").being.equal({
            'ordering': ['short_name'],
            'search': ['cool'],
            'period_short_name': ['spriing'],
            'subject_short_name': ['duck1010'],
            'short_name': ['superCool'],
            'id': ['1']
        })

    @httpretty.activate
    def test_assignment_list(self):
        data = json.loads(mocks.assignment_list_mock_student_and_examiner)
        httpretty.register_uri(httpretty.GET, 'http://localhost:8000/api/assignment/student',
                               body=mocks.assignment_list_mock_student_and_examiner)
        assignment_list = AssignmentList(self.client, 'student')
        assignments = assignment_list.assignment_list
        self.assertEqual(len(assignments), 2)

        # First
        self.assertEqual(data[0]['short_name'], assignments[0].data['short_name'])
        self.assertEqual(data[0]['id'], assignments[0].data['id'])
        self.assertEqual(data[0]['long_name'], assignments[0].data['long_name'])
        self.assertEqual(data[0]['period_short_name'], assignments[0].data['period_short_name'])
        self.assertEqual(data[0]['publishing_time'], assignments[0].data['publishing_time'].isoformat())
        self.assertEqual(data[0]['subject_short_name'], assignments[0].data['subject_short_name'])

        # Second
        self.assertEqual(data[1]['short_name'], assignments[1].data['short_name'])
        self.assertEqual(data[1]['id'], assignments[1].data['id'])
        self.assertEqual(data[1]['long_name'], assignments[1].data['long_name'])
        self.assertEqual(data[1]['period_short_name'], assignments[1].data['period_short_name'])
        self.assertEqual(data[1]['publishing_time'], assignments[1].data['publishing_time'].isoformat())
        self.assertEqual(data[1]['subject_short_name'], assignments[1].data['subject_short_name'])


class TestAssignment(unittest.TestCase):

    def setUp(self):
        self.client = Client('http://localhost:8000/api/')
        self.client.auth()

    def test_examiner_url(self):
        assignment = Assignment(self.client, 'examiner', id=1)
        self.assertEqual(assignment.get_url(), 'assignment/examiner?id=1')

    @httpretty.activate
    def test_student_id_queryparam(self):
        assignment = Assignment(self.client, 'student', id=1)
        # Mock api response
        httpretty.register_uri(httpretty.GET, 'http://localhost:8000/api/assignment/student',
                               body='[]')
        self.assertIsNone(assignment.data)
        expect(httpretty.last_request()).to.have.property("querystring").being.equal({
            'id': ['1']
        })

    def test_assignment_data_passed(self):
        data = json.loads(mocks.assignment_mock_student_and_examiner)[0]
        assignment = Assignment(self.client, 'examiner', data=data)
        self.assertEqual(data['short_name'], assignment.data['short_name'])
        self.assertEqual(data['id'], assignment.data['id'])
        self.assertEqual(data['long_name'], assignment.data['long_name'])
        self.assertEqual(data['period_short_name'], assignment.data['period_short_name'])
        self.assertEqual(data['publishing_time'], assignment.data['publishing_time'])
        self.assertEqual(data['subject_short_name'], assignment.data['subject_short_name'])

    @httpretty.activate
    def test_assignment_data_fetched_by_id(self):
        data = json.loads(mocks.assignment_mock_student_and_examiner)[0]
        assignment = Assignment(self.client, 'student', id=1)
        httpretty.register_uri(httpretty.GET, 'http://localhost:8000/api/assignment/student',
                               body=mocks.assignment_mock_student_and_examiner)
        self.assertEqual(data['short_name'], assignment.data['short_name'])
        self.assertEqual(data['id'], assignment.data['id'])
        self.assertEqual(data['long_name'], assignment.data['long_name'])
        self.assertEqual(data['period_short_name'], assignment.data['period_short_name'])
        self.assertEqual(data['publishing_time'], assignment.data['publishing_time'].isoformat())
        self.assertEqual(data['subject_short_name'], assignment.data['subject_short_name'])
