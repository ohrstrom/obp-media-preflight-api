"""URLs module"""
from django.conf import settings
from django.conf.urls import url

from django.contrib.auth.views import logout


app_name = 'auth_extra'

urlpatterns = [
    url(r'^logout/$', logout, name='logout'),
]
