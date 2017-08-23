from django.contrib import admin

from .models import Check

@admin.register(Check)
class CheckAdmin(admin.ModelAdmin):

    save_on_top = True

    date_hierarchy = 'created'

    list_display = [
        '__str__',
        'task_id',
        'media_file',
        'created',
        'status',
    ]

    list_filter = [
        'status',
        'created',
    ]

