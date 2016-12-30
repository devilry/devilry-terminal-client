import unittest

from httmock import with_httmock

from devilry.api_client.client import Client
from devilry.api_client import exceptions
from tests.mocks import devilry_api


class TestApiClinetHTTPError(unittest.TestCase):

    def setUp(self):
        client = Client('http://localhost:8000/api/')
        client.auth()
        self.api = client.api('')

    @with_httmock(devilry_api.HTTPErrorMocks.response_400)
    def test_400_is_raised(self):
        with self.assertRaises(exceptions.HTTP400):
            self.api.get()
        with self.assertRaises(exceptions.HTTP400):
            self.api.post()
        with self.assertRaises(exceptions.HTTP400):
            self.api.put()
        with self.assertRaises(exceptions.HTTP400):
            self.api.patch()
        with self.assertRaises(exceptions.HTTP400):
            self.api.delete()

    @with_httmock(devilry_api.HTTPErrorMocks.response_401)
    def test_401_is_raised(self):
        with self.assertRaises(exceptions.HTTP401):
            self.api.get()
        with self.assertRaises(exceptions.HTTP401):
            self.api.post()
        with self.assertRaises(exceptions.HTTP401):
            self.api.put()
        with self.assertRaises(exceptions.HTTP401):
            self.api.patch()
        with self.assertRaises(exceptions.HTTP401):
            self.api.delete()

    @with_httmock(devilry_api.HTTPErrorMocks.response_403)
    def test_403_is_raised(self):
        with self.assertRaises(exceptions.HTTP403):
            self.api.get()
        with self.assertRaises(exceptions.HTTP403):
            self.api.post()
        with self.assertRaises(exceptions.HTTP403):
            self.api.put()
        with self.assertRaises(exceptions.HTTP403):
            self.api.patch()
        with self.assertRaises(exceptions.HTTP403):
            self.api.delete()

    @with_httmock(devilry_api.HTTPErrorMocks.response_404)
    def test_404_is_raised(self):
        with self.assertRaises(exceptions.HTTP404):
            self.api.get()
        with self.assertRaises(exceptions.HTTP404):
            self.api.post()
        with self.assertRaises(exceptions.HTTP404):
            self.api.put()
        with self.assertRaises(exceptions.HTTP404):
            self.api.patch()
        with self.assertRaises(exceptions.HTTP404):
            self.api.delete()

    @with_httmock(devilry_api.HTTPErrorMocks.response_405)
    def test_405_is_raised(self):
        with self.assertRaises(exceptions.HTTP405):
            self.api.get()
        with self.assertRaises(exceptions.HTTP405):
            self.api.post()
        with self.assertRaises(exceptions.HTTP405):
            self.api.put()
        with self.assertRaises(exceptions.HTTP405):
            self.api.patch()
        with self.assertRaises(exceptions.HTTP405):
            self.api.delete()

    @with_httmock(devilry_api.HTTPErrorMocks.response_429)
    def test_429_is_raised(self):
        with self.assertRaises(exceptions.HTTP429):
            self.api.get()
        with self.assertRaises(exceptions.HTTP429):
            self.api.post()
        with self.assertRaises(exceptions.HTTP429):
            self.api.put()
        with self.assertRaises(exceptions.HTTP429):
            self.api.patch()
        with self.assertRaises(exceptions.HTTP429):
            self.api.delete()

    @with_httmock(devilry_api.HTTPErrorMocks.response_500)
    def test_500_is_raised(self):
        with self.assertRaises(exceptions.HTTP500):
            self.api.get()
        with self.assertRaises(exceptions.HTTP500):
            self.api.post()
        with self.assertRaises(exceptions.HTTP500):
            self.api.put()
        with self.assertRaises(exceptions.HTTP500):
            self.api.patch()
        with self.assertRaises(exceptions.HTTP500):
            self.api.delete()

    @with_httmock(devilry_api.HTTPErrorMocks.response_503)
    def test_503_is_raised(self):
        with self.assertRaises(exceptions.HTTP503):
            self.api.get()
        with self.assertRaises(exceptions.HTTP503):
            self.api.post()
        with self.assertRaises(exceptions.HTTP503):
            self.api.put()
        with self.assertRaises(exceptions.HTTP503):
            self.api.patch()
        with self.assertRaises(exceptions.HTTP503):
            self.api.delete()
