from core.settings.common import *
from core.settings.overrides import *

DEBUG = True

ALLOWED_HOSTS = ['*']

SECRET_KEY = 'l18j_)59lg#^3w9v0*nc!x9)vm6x&h)1z9^t(-nk()$w_59=mh'

STRAVA_SECRET = os.environ['STRAVA_SECRET']
