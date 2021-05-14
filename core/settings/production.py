from core.settings.common import *
from core.settings.overrides import *

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration


DEBUG = False

sentry_sdk.init(
    integrations=[DjangoIntegration()],

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)

SECRET_KEY = os.environ['SECRET_KEY']
STRAVA_SECRET = os.environ['STRAVA_SECRET']
