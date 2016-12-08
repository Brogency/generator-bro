from os.path import dirname

ROOT_PATH = dirname(dirname(dirname(__file__)))

from .installed_apps import *
from .locale import *
from .settings import *
from .constance import *
from .dbmail import *
from .grappelli import *
from .celery import *

ALLOWED_HOSTS = ['*']

try:
    from local import *
except ImportError:
    pass
