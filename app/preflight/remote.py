# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import requests
import tenacity

from django.conf import settings


API_BASE_URL = getattr(settings, 'REMOTE_API_BASE_URL', None)
AUTH_TOKEN = getattr(settings, 'REMOTE_API_AUTH_TOKEN', None)


def APIClientException(Exception):
    def __init__(self, m):
        self.message = m
    def __str__(self):
        return self.message


class APIClient(object):

    def __init__(self, auth_token=AUTH_TOKEN):

        self.headers = {
            'user-agent': 'openbroadcast.org - preflight-api client/0.0.1',
            'Authorization': 'Token {}'.format(AUTH_TOKEN)
        }

    #@tenacity.retry(wait=tenacity.wait_exponential(multiplier=1, max=10), stop=tenacity.stop_after_attempt(5))
    def get(self, url, *args, **kwargs):
        kwargs['headers'] = self.headers
        r = requests.get(url, *args, **kwargs)
        # if r.status_code >= 300:
        #     raise APIClientException(r.status_code)
        return r

    #@tenacity.retry(wait=tenacity.wait_exponential(multiplier=1, max=10), stop=tenacity.stop_after_attempt(5))
    def post(self, url, *args, **kwargs):
        kwargs['headers'] = self.headers
        r = requests.post(url, *args, **kwargs)
        # if r.status_code >= 300:
        #     raise APIClientException(r.status_code)
        return r

    #@tenacity.retry(wait=tenacity.wait_exponential(multiplier=1, max=10), stop=tenacity.stop_after_attempt(5))
    def patch(self, url, *args, **kwargs):
        kwargs['headers'] = self.headers
        r = requests.patch(url, *args, **kwargs)
        # if r.status_code >= 300:
        #     raise APIClientException(r.status_code)
        return r
