from requests.exceptions import HTTPError


class HTTP400(HTTPError):
	"""
	Http400 Error Exception

	The server cannot or will not process the request due to
	an apparent client error e.g., malformed request syntax,
	invalid request message framing, or deceptive request routing).
	"""

    def __str__(self):

        return repr('400  Bad Request')


class HTTP401(HTTPError):
	"""
	Http401 Error Exception

	Similar to 403 Forbidden, but specifically for use when authentication 
	is required and has failed or has not yet been provided.
	The response must include a WWW-Authenticate header field containing
	a challenge applicable to the requested resource.
	"""

	def __str__(self):

		return repr('401 Unauthorized')


class HTTP403(HTTPError):
	"""
	Http403 Error Exception

	The request was a valid request, but the server is refusing to respond to it.
	403 error semantically means "unauthorized", i.e. the user does not 
	have the necessary permissions for the resource.
	"""

	def __str__(self):
		
		return repr('403 Forbidden')


class HTTP404(HTTPError):
	"""
	Http404 Error Exception

	The requested resource could not be found but may be available in the future.
	Subsequent requests by the client are permissible.
	"""

    def __str__(self):

        return repr('404 not Found occurred')

class HTTP503(HTTPError):
	"""
	Http503 Error Exception

	The server is currently unavailable (because it is overloaded or 
	down for maintenance). Generally, this is a temporary state.
	"""

	def __str__(self):

		return repr('503 Service Unavailable')