# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^check/$', views.check_list, name='check-list'),
    url(r'^check/(?P<uuid>[0-9A-Fa-f-]+)/$', views.check_detail, name='check-detail'),
]
