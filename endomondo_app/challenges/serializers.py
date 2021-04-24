from rest_framework import serializers

from .models.challenge import Challenge
from .models.team import Team
from .models.competitor import Competitor
from .models.stats import Stats


class CompetitorSerializer(serializers.ModelSerializer):
    external_id = serializers.CharField()
    name = serializers.SerializerMethodField()
    calories = serializers.SerializerMethodField()

    def get_name(self, obj):
        return obj.get_name()

    def get_calories(self, obj):
        try:
            stats = Stats.objects.get(challenge__id=self.context['challenge_id'], competitor__id=obj.id)
            return stats.calories
        except Stats.DoesNotExist:
            return 0

    class Meta:
        model = Competitor
        fields = ('id', 'name', 'external_id', 'calories')


class TeamSerializer(serializers.ModelSerializer):
    members = serializers.SerializerMethodField()
    calories = serializers.SerializerMethodField()

    def __init__(self, *argc, **argv):
        super().__init__(*argc, **argv)
        self.competitors = None

    def get_members(self, obj):
        return [
            CompetitorSerializer(comp, context={'challenge_id': obj.challenge.id}).data
            for comp in self.get_competitors(obj)
        ]

    def get_calories(self, obj):
        competitors = self.get_competitors(obj)
        stats = Stats.objects.filter(challenge__id=obj.challenge.id, competitor__in=competitors)
        return sum([stat.calories for stat in stats])

    def get_competitors(self, obj):
        return Competitor.objects.filter(teams__id=obj.id)

    class Meta:
        model = Team
        fields = ('id', 'name', 'challenge', 'members', 'calories')


class ChallengeDetailsSerializer(serializers.ModelSerializer):
    external_id = serializers.CharField()
    teams = serializers.SerializerMethodField()

    def get_teams(self, obj):
        teams = Team.objects.filter(challenge=obj.id)
        return TeamSerializer(teams, many=True).data

    class Meta:
        model = Challenge
        fields = ('id', 'title', 'start_date', 'end_date', 'parse_error', 'status_text', 'parse_date', 'external_id', 'teams')


class ChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = ('id', 'title', 'start_date')
