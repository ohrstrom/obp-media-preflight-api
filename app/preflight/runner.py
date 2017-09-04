# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import os
import shutil
import time
import subprocess
import tempfile
from django.conf import settings

log = logging.getLogger(__name__)

DEFAULT_LS_BINARY_PATH = '/home/preflight/.opam/system/bin/liquidsoap'
DEFAULT_FFPROBE_BINARY_PATH = '/usr/bin/ffprobe'

LS_BINARY_PATH = getattr(settings, 'LS_BINARY_PATH', DEFAULT_LS_BINARY_PATH)
FFPROBE_BINARY_PATH = getattr(settings, 'FFPROBE_BINARY_PATH', DEFAULT_FFPROBE_BINARY_PATH)


LS_DECODE_SCRIPT = """
set("log.stdout",true)
set("log.file",false)
set("log.level",3)
input = "{in_path}"
output = "{out_path}"
source = once(single(input))
source = audio_to_stereo(source)
clock.assign_new(sync=false,[source])
output.file(%wav(stereo=true, channels=2, samplerate=44100, samplesize=16, header=true), output, fallible=true, on_stop=shutdown, source)
"""


#######################################################################
# Preflight Runner
#######################################################################
class PreflightRunner(object):

    def __init__(self, path):
        self.working_dir = tempfile.mkdtemp()
        self.path = path

        self.checks = {}
        self.errors = {}


        print(self.working_dir)


    def cleanup(self):
        if os.path.isdir(self.working_dir):
            log.debug('cleanup working dir: {}'.format(self.working_dir))
            shutil.rmtree(self.working_dir)

    def ls_decode(self):

        script_path = os.path.join(self.working_dir, 'ls_decode.liq')
        out_path = os.path.join(self.working_dir, 'out.wav')

        print('********************')
        print(LS_DECODE_SCRIPT.format(
                in_path=self.path,
                out_path=out_path
            ))


        ###############################################################
        # decode media file with liquidsoap
        ###############################################################
        with open(script_path, 'w') as f:
            f.write(LS_DECODE_SCRIPT.format(
                in_path=self.path,
                out_path=out_path
            ))

        ls_decode_command = [
            LS_BINARY_PATH,
            '-f',
            script_path
        ]

        log.debug('running: {}'.format(' '.join(ls_decode_command)))

        ls_decode_result = subprocess.check_output(
            ls_decode_command,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )

        for line in str(ls_decode_result).split('\n'):

            if '[decoder:' in line and 'Method' in line:
                msg = 'Method {}'.format(line.split('Method ')[1])
                log.info(msg)
                self.checks['decode'] = 'ok'

            if '[decoder:' in line and 'Unable to decode ' in line:
                msg = 'Unable to decode {}'.format(line.split('Unable to decode')[1])
                log.warning(msg)
                self.errors['decode'] = msg


        ###############################################################
        # check if output exists
        ###############################################################
        if os.path.isfile(out_path):
            print('file exists')
            log.info('output file exists at expected path')
            self.checks['out_file'] = 'ok'

        else:
            log.warning('error reading output file')
            self.errors['out_file'] = 'error reading file'


        ###############################################################
        # get duration of decoded file
        ###############################################################
        ffprobe_duration_command = [
            FFPROBE_BINARY_PATH,
            '-v',
            'error',
            '-show_entries',
            'format=duration',
            '-of',
            'default=noprint_wrappers=1:nokey=1',
            out_path
        ]

        try:

            log.debug('running: {}'.format(' '.join(ffprobe_duration_command)))

            ffprobe_duration_result = subprocess.check_output(
                ffprobe_duration_command,
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )

            duration = float(ffprobe_duration_result.strip())
            log.info('duration by ffprobe: {}'.format(duration))
            self.checks['duration_preflight'] = duration

        except Exception as e:
            log.warning('unable to read duration')
            self.errors['duration_preflight'] = 'error reading duration'


    def run(self):

        self.ls_decode()

        self.cleanup()

        return {'checks': self.checks, 'errors': self.errors}
