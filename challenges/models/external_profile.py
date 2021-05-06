from django.db import models

from . import Competitor


class DataProviderType(models.TextChoices):
    ENDOMONDO = 'ENDOMONDO'
    STRAVA = 'STRAVA'


class ExternalProfile(models.Model):
    competitor = models.ForeignKey(Competitor, related_name='external_profiles', on_delete=models.CASCADE)
    kind = models.CharField(max_length=16, choices=DataProviderType.choices)
    external_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100, blank=True)
