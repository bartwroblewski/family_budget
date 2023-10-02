import os

from .base import *


DEBUG = False

# Wildcard is used here just to allow running prod setup locally.
# Populate with your real hosts.
ALLOWED_HOSTS = ['*']

STATIC_ROOT = os.path.join(
    os.path.dirname(BASE_DIR),
    'collected_static',
)
