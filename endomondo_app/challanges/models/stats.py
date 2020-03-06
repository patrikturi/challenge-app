from django.db import models

from challanges.models.challange import Challange
from challanges.models.competitor import Competitor


class Stats(models.Model):
    competitor = models.ForeignKey(Competitor, on_delete=models.CASCADE)
    challange = models.ForeignKey(Challange, on_delete=models.CASCADE)
    calories = models.IntegerField()

    @classmethod
    def get_or_create(cls, challenge, competitor):
        stats_found = Stats.objects.filter(challange=challenge, competitor=competitor)
        assert len(stats_found) < 2
        if len(stats_found) == 0:
            stats = Stats(challange=challenge, competitor=competitor)
        else:
            stats = stats_found[0]
        return stats
