from django.db import models

from challanges.models.team import Team


class Competitor(models.Model):

    endomondo_id = models.IntegerField()
    name = models.CharField(max_length=100, blank=True)
    display_name = models.CharField(max_length=100, blank=True)
    teams = models.ManyToManyField(Team)
