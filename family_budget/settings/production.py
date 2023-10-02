import os

from dotenv import load_dotenv

from .base import *


load_dotenv()

SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = False

# Wildcard is used here just to allow running prod setup locally.
# Populate with your real hosts.
ALLOWED_HOSTS = ['*']

STATIC_ROOT = os.path.join(
    os.path.dirname(BASE_DIR),
    'collected_static',
)
