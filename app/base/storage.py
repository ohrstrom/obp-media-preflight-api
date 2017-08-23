# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models

class OverwriteFileSystemStorage(FileSystemStorage):

    """
    Update get_available_name to remove any previously stored file (if any) before returning the name.
    """
    def get_available_name(self, name, **kwargs):
        self.delete(name)
        return name
