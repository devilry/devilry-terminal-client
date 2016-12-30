import unittest

from devilry.api_client.client import Client
from devilry.api_client import exceptions
import httpretty


class TestApiClientHeaders(unittest.TestCase):

    def setUp(self):
        self.client = Client('http://localhost:8000/api/')
        self.client.auth(key='61d4d0b047b4d753c29d1756a4a656045c7df521')
        self.api = self.client.api('')

    def test_api_key_in_header(self):
        self.assertEqual(self.api.headers, {'Authorization': 'Token 61d4d0b047b4d753c29d1756a4a656045c7df521'})

    def test_api_key_in_header_client(self):
        self.assertEqual(self.client.headers, {'Authorization': 'Token 61d4d0b047b4d753c29d1756a4a656045c7df521'})


class TestApiClientHTTPSuccess(unittest.TestCase):

    def setUp(self):
        client = Client('http://localhost:8000/api/')
        client.auth()
        self.api = client.api('')

    @httpretty.activate
    def test_200_hello_world(self):
        httpretty.register_uri(httpretty.GET, "http://localhost:8000/api/",
                               status=200, body='{"hello": "world"}', content_type='application/json')
        response = self.api.get()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"hello": "world"})

        httpretty.register_uri(httpretty.PUT, "http://localhost:8000/api/",
                               status=200, body='{"hello": "world"}', content_type='application/json')
        response = self.api.put()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"hello": "world"})

        httpretty.register_uri(httpretty.PATCH, "http://localhost:8000/api/",
                               status=200, body='{"hello": "world"}', content_type='application/json')
        response = self.api.patch()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"hello": "world"})

    @httpretty.activate
    def test_204_hello_world(self):
        httpretty.register_uri(httpretty.DELETE, "http://localhost:8000/api/", status=204)
        response = self.api.delete()
        self.assertEqual(response.status_code, 204)

    @httpretty.activate
    def test_201_hello_world(self):
        httpretty.register_uri(httpretty.POST, "http://localhost:8000/api/",
                               status=201, body='{"hello": "world"}', content_type='application/json')
        response = self.api.post()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"hello": "world"})


class TestApiClinetHTTPError(unittest.TestCase):

    def setUp(self):
        client = Client('http://localhost:8000/api/')
        client.auth()
        self.api = client.api('')

    def before(self, status):
        httpretty.register_uri(httpretty.GET, "http://localhost:8000/api/", status=status)
        httpretty.register_uri(httpretty.POST, "http://localhost:8000/api/", status=status)
        httpretty.register_uri(httpretty.PUT, "http://localhost:8000/api/", status=status)
        httpretty.register_uri(httpretty.PATCH, "http://localhost:8000/api/", status=status)
        httpretty.register_uri(httpretty.DELETE, "http://localhost:8000/api/", status=status)

    @httpretty.activate
    def test_400_is_raised(self):
        self.before(400)
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

    @httpretty.activate
    def test_401_is_raised(self):
        self.before(401)
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

    @httpretty.activate
    def test_403_is_raised(self):
        self.before(403)
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

    @httpretty.activate
    def test_404_is_raised(self):
        self.before(404)
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

    @httpretty.activate
    def test_405_is_raised(self):
        self.before(405)
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

    @httpretty.activate
    def test_429_is_raised(self):
        self.before(429)
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

    @httpretty.activate
    def test_500_is_raised(self):
        self.before(500)
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

    @httpretty.activate
    def test_503_is_raised(self):
        self.before(503)
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
