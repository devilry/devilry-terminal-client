from requests import api

from devilry_api import exceptions


class Api(object):
	"""
	This class is an api instance.

	Examples:
		api = Api('http://example.com/api/list-things/')
		api.get()

		headers = {'Authorization': 'Token some_api_key'}
		api = Api('http://example.com/api/list-things/')
		api.get()
	"""

	def __init__(self, url, headers=None):
		self.url = url
		self.headers = headers or {}

	def handle_errors(self, status_code):
		"""

		"""
		if status_code == 400:
			raise exceptions.HTTP400
		if status_code == 401:
			raise exceptions.HTTP401
		if status_code == 403:
			raise exceptions.HTTP403
		if status_code == 404:
			raise exceptions.HTTP404
		if status_code == 405:
			raise exceptions.HTTP405
		if status_code == 529:
			raise exceptions.HTTP429
		if status_code == 503:
			raise exceptions.HTTP503

	def get(self, **kwargs):
		response = api.get(self.url, headers=self.headers, **kwargs)
		self.handle_errors(response.status_code)
		return response.content

	def post(self, **kwargs):
		response = api.post(self.url, headers=self.headers, **kwargs)
		self.handle_errors(response.status_code)
		return response.content

	def update(self, **kwargs):
		response = api.update(self.url, headers=self.headers, **kwargs)
		self.handle_errors(response.status_code)
		return response.content

	def put(self, **kwargs):
		response = api.put(self.url, headers=self.headers, **kwargs)
		self.handle_errors(response.status_code)
		return response.content

	def patch(self, **kwargs):
		response = api.patch(self.url, headers=self.headers, **kwargs)
		self.handle_errors(response.status_code)
		return response.content
