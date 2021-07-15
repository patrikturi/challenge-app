import time

from django.db import models

from challenges.models import ExternalProfile
from strava.strava_api import get_token


class StravaToken(models.Model):
    profile = models.ForeignKey(ExternalProfile, on_delete=models.CASCADE)
    _access_token = models.CharField(max_length=100)
    refresh_token = models.CharField(max_length=100)
    expires_at = models.IntegerField()

    @property
    def access_token(self):
        if not self.is_valid():
            self.refresh()
        return self._access_token

    @access_token.setter
    def access_token(self, value):
        self._access_token = value

    def is_valid(self):
        return self.expires_at - int(time.time()) > 0

    # https://developers.strava.com/docs/authentication/#refreshingexpiredaccesstokens
    def refresh(self):
        token = get_token('refresh_token', self.refresh_token)
        self._access_token = token['access_token']
        self.expires_at = token['expires_at']
        self.save()
