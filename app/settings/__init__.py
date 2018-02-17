# -*- coding: utf-8 -*-
import os
import sys
from split_settings.tools import optional, include

SITE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
APP_ROOT = os.path.join(SITE_ROOT, 'app')

sys.path.insert(0, APP_ROOT)

#
gettext = lambda s: s
_ = gettext

# dev & test
RUNNING_DEVSERVER = (len(sys.argv) > 1 and sys.argv[1] == 'runserver')

include(
    'components/base.py',
    'components/template.py',

    # optional local settings
    optional(os.path.join(APP_ROOT, 'local_settings.py')),

    # via server based settings in etc (placed by ansible deployment tasks)
    optional('/etc/preflight-api/application-settings.py'),
    optional('/etc/preflight-api/logging.py'),
    scope=locals()
)
