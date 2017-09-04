from __future__ import absolute_import

import logging
import json
import time
import tenacity

from celery import shared_task

from .remote import APIClient
from .runner import PreflightRunner

log = logging.getLogger(__name__)


@shared_task
def preflight_check_task(obj):

    log.debug('run preflight check for {}'.format(obj.pk))

    r = PreflightRunner(obj.media_file.path)

    preflight_result = r.run()


    if preflight_result['errors']:
        obj.status = obj.STATUS_ERROR
    else:
        obj.status = obj.STATUS_DONE


    obj.task_id = None
    obj.save()

    # inform remote api
    url = obj.remote_uri

    log.debug('updating remote resource: {}'.format(url))

    r = APIClient().patch(
        url,
        json={'result': json.dumps(preflight_result)}
    )

    log.debug('API response status code: {}'.format(r.status_code))
    log.debug('API response text: {}'.format(r.text))

    log.debug('check done - delete instance')
    obj.delete()





"""
# The input file,
# any format supported by liquidsoap
input = "/tmp/input.mp3"

# The output file
output = "/tmp/output.ogg"

# A source that plays the file once
source = once(single(input))

# We use a clock with disabled synchronization
clock.assign_new(sync=false,[source])

# Finally, we output the source to an
# ogg/vorbis file
output.file(%vorbis, output,fallible=true,
                     on_stop=shutdown,source)
"""



"""
input = "/data/preflight-api/media/preflight/0788444f-0048-4257-8975-4c8c86fa6692/418468.m4a"
output = "/tmp/output.ogg"
source = once(single(input))
clock.assign_new(sync=false,[source])
output.file(%vorbis, output, fallible=true, on_stop=shutdown, source)
"""



"""
set("log.stdout",true)
set("log.file",false)
input = "/data/preflight-api/media/preflight/0788444f-0048-4257-8975-4c8c86fa6692/418468.m4a"
output = "/tmp/output.ogg"
source = once(single(input))
clock.assign_new(sync=false,[source])
output.file(%vorbis, output, fallible=true, on_stop=shutdown, source)
"""
