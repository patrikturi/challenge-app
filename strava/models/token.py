from django.db import models
from challenges.models import ExternalProfile

class StravaToken(models.Model):
    profile = models.ForeignKey(ExternalProfile, on_delete=models.CASCADE)
    _access_token = models.CharField(max_length=100)
    refresh_token = models.CharField(max_length=100)
    expires_at = models.IntegerField()

