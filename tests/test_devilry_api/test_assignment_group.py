import unittest
import httpretty
import json
from sure import expect
from devilry.devilry_api import AssignmentGroupList, AssignmentGroup
from devilry.api_client import Client
from helpers import mocks


class TestAssignmentGroupList(unittest.TestCase):

    def setUp(self):
        self.client = Client('http://localhost:8000/api/')
        self.client.auth()

    def test_examiner_url(self):
        group = AssignmentGroupList(self.client, 'examiner')
        self.assertEqual(group.get_url(), 'assignment-group/examiner')

    def test_student_url(self):
        group = AssignmentGroupList(self.client, 'student')
        self.assertEqual(group.get_url(), 'assignment-group/student')

    @httpretty.activate
    def test_student_with_queryparams(self):
        group_list = AssignmentGroupList(
            self.client,
            'student',
            ordering='short_name',
            search='cool',
            period_short_name='spriing',
            subject_short_name='duck1010',
            assignment_short_name='superCool',
            id='1',
            assignment_id=2
        )
        httpretty.register_uri(httpretty.GET, 'http://localhost:8000/api/assignment-group/student', body='[]')
        list = group_list.assignment_group_list
        self.assertIsNone(list)
        expect(httpretty.last_request()).to.have.property("querystring").being.equal({
            'ordering': ['short_name'],
            'search': ['cool'],
            'period_short_name': ['spriing'],
            'subject_short_name': ['duck1010'],
            'assignment_short_name': ['superCool'],
            'id': ['1'],
            'assignment_id': ['2']
        })

    @httpretty.activate
    def test_assignment_group_list(self):
        data = json.loads(mocks.assignment_group_list_mock_student_and_examiner)
        httpretty.register_uri(httpretty.GET, 'http://localhost:8000/api/assignment-group/examiner',
                               body=mocks.assignment_group_list_mock_student_and_examiner)
        group_list = AssignmentGroupList(self.client, 'examiner')
        groups = group_list.assignment_group_list
        self.assertEqual(len(groups), 2)

        # First
        self.assertDictEqual(data[0], groups[0].data)

        # Second
        self.assertDictEqual(data[1], groups[1].data)


class TestAssignmentGroup(unittest.TestCase):

    def setUp(self):
        self.client = Client('http://localhost:8000/api/')
        self.client.auth()

    def test_examiner_url(self):
        group = AssignmentGroup(self.client, 'examiner', id=1)
        self.assertEqual(group.get_url(), 'assignment-group/examiner?id=1')

    @httpretty.activate
    def test_student_id_queryparam(self):
        group = AssignmentGroup(self.client, 'student', id=1)
        # Mock api response
        httpretty.register_uri(httpretty.GET, 'http://localhost:8000/api/assignment-group/student',
                               body='[]')
        self.assertIsNone(group.data)
        expect(httpretty.last_request()).to.have.property("querystring").being.equal({
            'id': ['1']
        })

    def test_assignment_group_data_passed_url_and_data(self):
        data = json.loads(mocks.assignment_group_list_mock_student_and_examiner)[0]
        group = AssignmentGroup(self.client, 'student', data=data)
        self.assertEqual(group.get_url(), 'assignment-group/student?id={}'.format(data['id']))
        self.assertDictEqual(group.data, data)

    @httpretty.activate
    def test_assignment_data_fetched_by_id(self):
        data = json.loads(mocks.assignment_group_mock_student_and_examiner)[0]
        group = AssignmentGroup(self.client, 'examiner', id=1)
        httpretty.register_uri(httpretty.GET, 'http://localhost:8000/api/assignment-group/examiner',
                               body=mocks.assignment_group_mock_student_and_examiner)
        self.assertDictEqual(data, group.data)
