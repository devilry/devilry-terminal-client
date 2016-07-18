import unittest

import argparse
from devilryclientlib.plugin import BaseApiPlugin


class TestBaseApiPlugin(unittest.TestCase):

    def setUp(self):
        self.testClass = BaseApiPlugin()
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('-s', dest='search')
        self.parser.add_argument('-n', dest='name')
        self.parser.add_argument('-o', dest='ordering')

    def test_parse_queryparms_no_queryparams(self):
        self.testClass.queryparams = []
        query = self.testClass.parse_queryparams(self.parser.parse_args([]))
        self.assertEqual(query, '')

    def test_parse_queryparams_no_args(self):
        self.testClass.queryparams = ['search', 'name', 'ordering']
        query = self.testClass.parse_queryparams(self.parser.parse_args([]))
        self.assertEqual(query, '')

    def test_parse_queryparams_query_string(self):
        self.parser.add_argument('-qs', dest='query_string')
        args = ['-qs', '?search=hey&ordering=name']
        query = self.testClass.parse_queryparams(self.parser.parse_args(args))
        self.assertEqual(query, '?search=hey&ordering=name')

    def test_parse_queryparams_query_string_and_argument(self):
        self.parser.add_argument('-qs', dest='query_string')
        args = ['-qs', '?search=hey&ordering=name', '-o', 'date']
        query = self.testClass.parse_queryparams(self.parser.parse_args(args))
        self.assertEqual(query, '?search=hey&ordering=name')

    def test_parse_queryparams_one_argument(self):
        self.testClass.queryparams = ['search', 'name', 'ordering']
        args = ['-o', 'name']
        query = self.testClass.parse_queryparams(self.parser.parse_args(args))
        self.assertEqual(query, '?ordering=name')

    def test_parse_queryparams_multiple_arguments(self):
        self.testClass.queryparams = ['search', 'name', 'ordering']
        args = ['-o', 'date', '-s', 'hey', '-n', 'imba']
        query = self.testClass.parse_queryparams(self.parser.parse_args(args))
        self.assertEqual(query, '?search=hey&name=imba&ordering=date')
