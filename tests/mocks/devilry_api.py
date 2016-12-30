# -*- coding: utf-8 -*-

"""
Mocks for devilry api
"""

from httmock import response, urlmatch


class HTTPErrorMocks:
    @urlmatch()
    def response_400(url, request):
        return {'status_code': 400}

    @urlmatch()
    def response_401(url, request):
        return {'status_code': 401}

    @urlmatch()
    def response_403(url, request):
        return {'status_code': 403}

    @urlmatch()
    def response_404(url, request):
        return {'status_code': 404}

    @urlmatch()
    def response_405(url, request):
        return {'status_code': 405}

    @urlmatch()
    def response_429(url, request):
        return {'status_code': 429}

    @urlmatch()
    def response_500(url, request):
        return {'status_code': 500}

    @urlmatch()
    def response_503(url, request):
        return {'status_code': 503}
