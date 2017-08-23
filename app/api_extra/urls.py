# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^status/$', views.APIStatusView.as_view(), name='api-status'),
]
