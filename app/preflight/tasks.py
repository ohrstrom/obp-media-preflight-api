from __future__ import absolute_import

import logging
import time

from celery import shared_task
from django.core.files import File

from .remote import APIClient
from .runner import PreflightRunner

log = logging.getLogger(__name__)


@shared_task
def preflight_check_task(obj):

    log.debug('run preflight check for {}'.format(obj.pk))

    print('**********')
    print(obj.media_file.path)




    r = PreflightRunner(obj.media_file.path)

    preflight_result = r.run()


    print('*************************')
    print(preflight_result)
    print('*************************')



    # r = Renderer()
    #
    # obj._skip_content_hash_check = True
    #
    # try:
    #
    #     mixdown_path = r.render(playlist_id=obj.pk, playlist_uri=obj.remote_uri)
    #
    #     with open(mixdown_path, 'rb') as f:
    #         mixdown_file = File(f)
    #         obj.status = obj.STATUS_DONE
    #
    #         obj.mixdown_file.save('mixdown.mp3', mixdown_file, False)
    #
    #     log.info('successfully rendered playlist id: {}'.format(obj.pk))
    #
    #
    # except Exception as e:
    #
    #     log.error('error rendering playlist id: {} - {}'.format(obj.pk, e))
    #     obj.status = obj.STATUS_ERROR

    # cleans all renderer artefacts
    # r.cleanup()


    print('pre-sleep')
    time.sleep(0.1)
    obj.status = obj.STATUS_DONE
    print('post-sleep')


    obj.task_id = None
    obj.save()

    # inform remote api
    #url = '{}{}'.format(obj.remote_uri, 'mixdown-complete/')
    #r = APIClient().post(url, data=[])

    # print(r.status_code)
