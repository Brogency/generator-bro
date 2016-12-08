import dj_database_url
import logging
import os

SECRET_KEY = "dkf)^fdo5_xenbz)z1jw69i0cew98oo18z3o-pzm$2^_8aalr#"

ANONYMOUS_USER_ID = -1
SITE_ID = 1
ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

##################################################################
# Debug settings
##################################################################

DEBUG = os.environ.get('DEBUG', 'True') == 'True'

TEMPLATE_DEBUG = DEBUG

if DEBUG:
    def show_toolbar(request):
        return True


    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK": show_toolbar,
    }

##################################################################
# Databases settings (for docker)
##################################################################

DATABASES = {'default': dj_database_url.config()}

##################################################################
# Logging settings
##################################################################

LOG_DATE_FORMAT = '%d %b %Y %H:%M:%S'

LOG_FORMATTER = logging.Formatter(
    u'%(asctime)s | %(levelname)-7s | %(name)s | %(message)s',
    datefmt=LOG_DATE_FORMAT)

CONSOLE_HANDLER = logging.StreamHandler()

CONSOLE_HANDLER.setFormatter(LOG_FORMATTER)

CONSOLE_HANDLER.setLevel(logging.DEBUG)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'sentry': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'raven_error': {
            'level': 'ERROR',
            'handlers': ['sentry'],
            'propagate': False,
        },
    }
}

##################################################################
# Assets settings
##################################################################

from os.path import dirname, basename, join

SETTINGS_PATH = dirname(__file__)
PROJECT_PATH = dirname(SETTINGS_PATH)
PROJECT_NAME = basename(PROJECT_PATH)
SERVER_PATH = dirname(PROJECT_PATH)
ROOT_PATH = dirname(SERVER_PATH)

FILE_UPLOAD_PERMISSIONS = 0o644

STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = STATIC_URL
MEDIA_ROOT = join(SERVER_PATH, 'media')
MEDIA_URL = '/media/'
STATICFILES_DIRS = ('static',)
TEMPLATE_DIRS = ('templates',)
REDACTOR_UPLOAD = 'content/'
FLATBLOCKS_AUTOCREATE_STATIC_BLOCKS = True

##################################################################
# Finders, loaders, middleware and context processors
##################################################################

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
)

CORS_ORIGIN_ALLOW_ALL = True


##################################################################
# REST framework settings
##################################################################
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    )
}


##################################################################
# REDIS settings
##################################################################
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get('REDIS_URL'),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            'MAX_ENTRIES': 10000,
        },
    }
}


##################################################################
# CELERY tasks (with example)
##################################################################
from celery.schedules import crontab
CELERYBEAT_SCHEDULE = {
    # 'every-1-min-add-example-object': {
    #     'task': 'apps.example_app.tasks.add_example',
    #     'schedule': crontab(minute='*/1'),
    # },
}


##################################################################
# SENTRY settings (you need paste SENTRY_DSN in docker-compose.yml)
##################################################################
SENTRY_DSN = os.environ.get('SENTRY_DSN', '')

RAVEN_CONFIG = {
    'dsn': SENTRY_DSN,
}