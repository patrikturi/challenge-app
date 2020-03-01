from django.db import models
from django.forms.models import model_to_dict

from challanges.models.challange import Challange


class Team(models.Model):

    name = models.CharField(max_length=100)
    challange = models.ForeignKey(Challange, on_delete=models.CASCADE)

    def to_dict(self):
        from challanges.models.competitor import Competitor

        competitors = Competitor.objects.filter(teams__id=self.id)

        competitor_dicts = [comp.to_dict(self.challange.id) for comp in competitors]
        team_calories = 0
        for comp in competitor_dicts:
            team_calories += comp['calories']

        team_dict = model_to_dict(self)
        team_dict['members'] = competitor_dicts
        team_dict['calories'] = team_calories
        return team_dict

    def __str__(self):
        return 'Team "{}"'.format(self.name)
