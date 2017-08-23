INTERNAL_IPS = (
    '127.0.0.1',
    '10.40.10.40',
)

DEBUG = True

SITE_URL = 'http://j.h612.anorg.net'



# TEMPLATES[0]['OPTIONS']['loaders'] = [
#     'django.template.loaders.filesystem.Loader',
#     'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
# ]


##################################################################
# db
##################################################################
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'preflight_api_local',
        'USER': 'ohrstrom',
        'HOST': '',
    }
}


##################################################################
# cache
##################################################################
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
}
CACHALOT_ENABLED = True
CACHALOT_CACHE = 'cachalot'

# SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
# SESSION_CACHE_ALIAS = 'default'


# CACHES = {
#     'default': {
#         'BACKEND': 'redis_cache.RedisCache',
#         'LOCATION': [
#             'localhost:6379',
#         ],
#         'OPTIONS': {
#             'DB': 3,
#         },
#     },
#     'cachalot': {
#         'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
#     }
# }
#
# CACHALOT_CACHE = 'cachalot'
# CACHALOT_ENABLED = True

##################################################################
# queues
##################################################################
CELERY_BROKER_URL = 'redis://localhost:6379/6'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/6'
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_ACCEPT_CONTENT = ['json', 'pickle']



##################################################################
# email
##################################################################
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = '***'
EMAIL_HOST_PASSWORD = '***'
EMAIL_PORT = 587
EMAIL_USE_TLS = True



##################################################################
# staticfiles through whitenose & cloud front
##################################################################


STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
WHITENOISE_MAX_AGE = 60


#MEDIA_URL = 'http://hoodeenie.j.h612.anorg.net/media/'
#STATIC_URL = 'http://hoodeenie.j.h612.anorg.net/static/'


COMPRESS_ENABLED = False
COMPRESS_OFFLINE = False

COMPRESS_OFFLINE_CONTEXT = {
    'template': 'base.html',
}


INSTALLED_APPS += [
    'debug_toolbar',
    'django_extensions',
    #'devserver',
]

MIDDLEWARE_CLASSES += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    #'devserver.middleware.DevServerMiddleware',
    #'base.middleware.profile.ProfileMiddleware',
]

DEBUG_TOOLBAR_PANELS = [

]

WERKZEUG_DEBUG_PIN = 'off'


##################################################################
# API
##################################################################
REST_FRAMEWORK['DEFAULT_PERMISSION_CLASSES'] = [
    'rest_framework.permissions.AllowAny',
]

#DEVSERVER_IGNORED_PREFIXES = ['/media', '/static']

DEVSERVER_MODULES = (
    'devserver.modules.profile.ProfileSummaryModule',

    # Modules not enabled by default
    'devserver.modules.ajax.AjaxDumpModule',
    'devserver.modules.profile.MemoryUseModule',
    'devserver.modules.cache.CacheSummaryModule',
    'devserver.modules.profile.LineProfilerModule',
)



from colorlog import ColoredFormatter
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s %(lineno)-4s [%(levelname)s] %(name)s: %(message)s'
        },
        'debug': {
            'format': '[%(levelname)s] %(name)s: %(message)s'
        },
        'colored': {
            '()': 'colorlog.ColoredFormatter',
            'format': '%(log_color)s%(asctime)s %(lineno)-4s%(name)-24s %(levelname)-8s %(message)s',
            'log_colors': {
                'DEBUG': 'cyan',
                'INFO': 'bold_green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red',
            },
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'colored',
        },
    },
    'loggers': {

        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console',],
            'propagate': False
        },
        '': {
            'handlers': ['console',],
            'level': 'ERROR',
            'propagate': False
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False
        },
        'matching': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False
        },
        'notification': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'flatshare': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'celery': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False
        },
        'dev': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}


# MATCHING_SKIP_UPDATE = True
MATCHING_ALWAYS_UPDATE = True
MATCHING_RUN_ASYNC = False


EL_PAGINATION_PER_PAGE = 24

PLACEHOLDER_IMAGE_DEFAULT_COLOR = '#333333'


SENDGRID_EVENTS_IGNORE_MISSING = True
NOTIFICATION_EMAIL_RUN_ASYNC = False


LOADERIO_TOKEN = '1fbbd921ffd3a8bcee22d45909db83c0'


REMOTE_API_BASE_URL = 'http://local.openbroadcast.org:8000'
REMOTE_API_AUTH_TOKEN = '35bd7543edc2150ce4e2902b5d3e71f220856989'
