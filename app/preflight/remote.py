import requests

from django.conf import settings


API_BASE_URL = getattr(settings, 'REMOTE_API_BASE_URL')
AUTH_TOKEN = getattr(settings, 'REMOTE_API_AUTH_TOKEN', None)

class APIClient(object):

    def __init__(self, auth_token=AUTH_TOKEN):

        self.headers = {
            'user-agent': 'openbroadcast.org - preflight-api client/0.0.1',
            'Authorization': 'Token {}'.format(AUTH_TOKEN)
        }

    def get(self, url, *args, **kwargs):
        kwargs['headers'] = self.headers
        return requests.get(url, *args, **kwargs)

    def post(self, url, data, *args, **kwargs):
        kwargs['headers'] = self.headers
        return requests.post(url, data, *args, **kwargs)
