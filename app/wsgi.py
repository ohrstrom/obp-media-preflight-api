# import os
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
#
# from django.core.wsgi import get_wsgi_application
# application = get_wsgi_application()

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
application = get_wsgi_application()
