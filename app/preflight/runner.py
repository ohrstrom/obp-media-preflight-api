# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import os
import shutil
import subprocess
import tempfile


log = logging.getLogger(__name__)

LS_BINARY_PATH = '/home/preflight/.opam/system/bin/liquidsoap'


LS_DECODE_SCRIPT = """
set("log.stdout",true)
set("log.file",false)
input = "{in_path}"
output = "{out_path}"
source = once(single(input))
clock.assign_new(sync=false,[source])
output.file(%vorbis, output, fallible=true, on_stop=shutdown, source)
"""


#######################################################################
# Preflight Runner
#######################################################################
class PreflightRunner(object):

    checks = []
    errors = []

    def __init__(self, path):
        self.working_dir = tempfile.mkdtemp()
        self.path = path
        print(self.working_dir)


    def __exit__(self, exc_type, exc_value, traceback):
        if os.path.isdir(self.working_dir):
            print(self.working_dir)
            #shutil.rmtree(self.working_dir)

    def ls_decode(self):

        checks = []
        errors = []

        script_path = os.path.join(self.working_dir, 'ls_decode.liq')
        out_path = os.path.join(self.working_dir, 'out.wav')

        print('********************')
        print(LS_DECODE_SCRIPT.format(
                in_path=self.path,
                out_path=out_path
            ))


        with open(script_path, 'w') as f:
            f.write(LS_DECODE_SCRIPT.format(
                in_path=self.path,
                out_path=out_path
            ))



        command = [
            LS_BINARY_PATH,
            '-f',
            script_path
        ]

        log.debug('running: {}'.format(' '.join(command)))

        process = subprocess.Popen(command, stdout=subprocess.PIPE)
        process.wait()

        checks.append({
            'return_code': process.returncode
        })


        self.errors += errors
        self.checks += checks


    def run(self):

        self.ls_decode()

        return {'checks': self.checks, 'errors': self.errors}
