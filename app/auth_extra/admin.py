# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from auth_extra.models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    save_on_top = True
