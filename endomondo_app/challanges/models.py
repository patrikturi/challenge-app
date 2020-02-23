from django.db import models


class Challange(models.Model):

    endomondo_id = models.IntegerField()
    name = models.CharField(max_length=200, blank=True)
    start_date = models.DateTimeField('Start date', null=True)
    end_date = models.DateTimeField('End date', null=True)


class Team(models.Model):

    name = models.CharField(max_length=100)
    challange = models.ForeignKey(Challange, on_delete=models.CASCADE)


class Competitor(models.Model):

    endomondo_id = models.IntegerField()
    name = models.CharField(max_length=100, blank=True)
    display_name = models.CharField(max_length=100, blank=True)
    teams = models.ManyToManyField(Team)


class Calories(models.Model):
    competitor = models.ForeignKey(Competitor, on_delete=models.CASCADE)
    challenge_id = models.ForeignKey(Challange, on_delete=models.CASCADE)
    kcal = models.IntegerField()
