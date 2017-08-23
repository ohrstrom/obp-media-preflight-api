from __future__ import unicode_literals

import json
import urllib

from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import View
