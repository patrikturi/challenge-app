from project.settings.common import *

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration


DEBUG = False

SECRET_KEY = os.environ['SECRET_KEY']

ALLOWED_HOSTS = ['*']

sentry_sdk.init(
    integrations=[DjangoIntegration()],

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)

ENDOMONDO_USERNAME = os.environ['ENDOMONDO_USER']
ENDOMONDO_PASSWORD = os.environ['ENDOMONDO_PASSWORD']
