from django.db import models

from challenges.models import Challenge, Competitor


class Stats(models.Model):
    competitor = models.ForeignKey(Competitor, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    calories = models.IntegerField()

    @classmethod
    def get_or_create(cls, challenge, competitor):
        stats_found = Stats.objects.filter(challenge=challenge, competitor=competitor)
        assert len(stats_found) < 2
        if len(stats_found) == 0:
            stats = Stats(challenge=challenge, competitor=competitor)
        else:
            stats = stats_found[0]
        return stats
