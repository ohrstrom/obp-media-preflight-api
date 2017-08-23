# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import os
import shutil
import subprocess
import tempfile


log = logging.getLogger(__name__)


#######################################################################
# Preflight Runner
#######################################################################
class PreflightRunner(object):

    checks = []
    errors = []

    def __init__(self, path):
        self.path = path

    def ls_decode(self):
        checks = []
        errors = []

        self.errors += errors
        self.checks += checks


    def run(self):

        self.ls_decode()

        return {'checks': self.checks, 'errors': self.errors}
