from django.db import models

from challenges.models import Challenge, Competitor


class StatTypes(models.TextChoices):
    SPORT = 'SPORT'
    WALK = 'WALK'
    RUN = 'RUN'
    SWIM = 'SWIM'
    BIKE = 'BIKE'
    HIKE = 'HIKE'


class StatUnits(models.TextChoices):
    CALORIES = 'CALORIES'
    KILOMETERS = 'KILOMETERS'


class Stats(models.Model):
    competitor = models.ForeignKey(Competitor, related_name='stats', on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, related_name='stats', on_delete=models.CASCADE)
    kind = models.CharField(max_length=16, choices=StatTypes.choices)
    unit = models.CharField(max_length=16, choices=StatUnits.choices)
    value = models.IntegerField(default=0)
    external_id = models.IntegerField(default=0)
    external_datetime = models.DateTimeField(null=True)