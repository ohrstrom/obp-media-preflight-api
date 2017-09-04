# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

from app import __version__

class APIStatusView(APIView):
    """
    exposes status & version information.
    version corresponds to the global app version.
    """
    # authentication_classes = []

    def get(self, request, format=None):

        data = {
            'status': {},
            'version': __version__
        }

        return Response(data)
