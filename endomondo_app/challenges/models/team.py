from django.db import models

from challenges.models import Challenge


class Team(models.Model):

    name = models.CharField(max_length=100)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)

    def __str__(self):
        return 'Team "{}"'.format(self.name)
