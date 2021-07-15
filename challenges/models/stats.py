from django.db import models

from challenges.models import Challenge, Competitor


class StatTypes(models.TextChoices):
    SPORT = 'SPORT'
    WALK = 'WALK'
    RUN = 'RUN'
    SWIM = 'SWIM'
    BIKE = 'BIKE'
    HIKE = 'HIKE'

STRAVA_STAT_TYPES = [StatTypes.WALK.value, StatTypes.RUN.value, StatTypes.SWIM.value, StatTypes.BIKE.value, StatTypes.HIKE.value]

class StatUnits(models.TextChoices):
    CALORIES = 'CALORIES'
    METERS = 'METERS'


class Stats(models.Model):
    competitor = models.ForeignKey(Competitor, related_name='stats', on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, null=True, related_name='stats', on_delete=models.CASCADE)
    kind = models.CharField(max_length=16, choices=StatTypes.choices)
    unit = models.CharField(max_length=16, choices=StatUnits.choices)
    value = models.IntegerField(default=0)
    external_id = models.IntegerField(default=0)
    external_datetime = models.DateTimeField(null=True)
