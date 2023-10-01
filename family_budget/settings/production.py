import os

from .base import *


DEBUG = False

# wilcard is used here just to allow running prod setup locally
ALLOWED_HOSTS = ['*']

STATIC_ROOT = os.path.join(
    os.path.dirname(BASE_DIR),
    'collected_static',
)
