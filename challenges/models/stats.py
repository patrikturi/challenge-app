from django.db import models

from challenges.models import Challenge, Competitor


class Stats(models.Model):
    competitor = models.ForeignKey(Competitor, related_name='stats', on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, related_name='stats', on_delete=models.CASCADE)
    calories = models.IntegerField(default=0)
