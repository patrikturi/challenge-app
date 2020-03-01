from django.db import models
from django.forms.models import model_to_dict


class Challange(models.Model):

    endomondo_id = models.IntegerField()
    title = models.CharField(max_length=200, blank=True)
    start_date = models.DateTimeField('Start date', null=True, blank=True)
    end_date = models.DateTimeField('End date', null=True, blank=True)

    def to_short_dict(self):
        return {'id': self.id, 'title': self.title, 'start_date': self.start_date}

    # View of the model. Would be better to use eg. restframework but this was the lowest effort
    def to_dict(self):
        # Avoids circular imports
        from challanges.models.team import Team
        from challanges.models.competitor import Competitor
        from challanges.models.stats import Stats

        teams = Team.objects.filter(challange=self)

        team_dicts = []
        for team in teams:
            competitors = Competitor.objects.filter(teams__id=team.id)

            competitors_list = [comp.to_dict() for comp in competitors]
            team_calories = 0
            for comp in competitors_list:
                if 'teams' in comp:
                    del comp['teams']
                try:
                    stats = Stats.objects.get(challange__id=self.id, competitor__id=comp['id'])
                    comp['calories'] = stats.calories
                    team_calories += stats.calories
                except Stats.DoesNotExist:
                    comp['calories'] = 0

            team_dict = model_to_dict(team)
            
            team_dict['members'] = competitors_list
            team_dict['calories'] = team_calories

            team_dicts.append(team_dict)

        challange_dict = model_to_dict(self)
        challange_dict['teams'] = team_dicts
        return challange_dict

    def __str__(self):
        name = '"{}"'.format(self.title) if self.title else self.endomondo_id
        return 'Challange {}'.format(name)
