from django.db.models import Prefetch
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from .models.challenge import Challenge
from .models.competitor import Competitor
from .models.stats import Stats
from .models.team import Team


class CompetitorSerializer(serializers.ModelSerializer):
    external_id = serializers.CharField()
    name = serializers.SerializerMethodField()
    score = serializers.SerializerMethodField()
    external_url = serializers.SerializerMethodField()

    def get_name(self, obj):
        return obj.get_name()

    def get_score(self, obj):
        try:
            return sum(stat.value for stat in obj.stats.all())
        except Stats.DoesNotExist:
            return 0

    def get_external_url(self, obj):
        return self.context['provider'].get_competitor_url(obj.external_id)

    class Meta:
        model = Competitor
        fields = ('id', 'name', 'external_id', 'score', 'external_url')


class TeamSerializer(serializers.ModelSerializer):
    members = serializers.SerializerMethodField()
    score = serializers.SerializerMethodField()

    def __init__(self, *argc, **argv):
        super().__init__(*argc, **argv)
        self.competitors = None

    def get_members(self, obj):
        return [
            CompetitorSerializer(comp, context={'provider': self.context['provider'], 'challenge_id': obj.challenge_id}).data
            for comp in obj.competitors.all()
        ]

    def get_score(self, obj):
        return sum([
            sum([stat.value for stat in comp.stats.all()])
            for comp in obj.competitors.all()
        ])

    def get_competitors(self, obj):
        return Competitor.objects.filter(teams__id=obj.id)

    class Meta:
        model = Team
        fields = ('id', 'name', 'challenge', 'members', 'score')


class ChallengeDetailsSerializer(serializers.ModelSerializer):
    external_id = serializers.CharField()
    teams = serializers.SerializerMethodField()
    provider = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._provider = None

    def get_teams(self, obj):
        teams = Team.objects.filter(challenge=obj).prefetch_related('competitors') \
                .prefetch_related(Prefetch('competitors__stats', queryset=Stats.objects.filter(challenge=obj)))
        return TeamSerializer(teams, context={'provider': obj.provider}, many=True).data

    def get_provider(self, obj):
        return obj.provider.to_representation()

    class Meta:
        model = Challenge
        fields = ('id', 'title', 'start_date', 'end_date', 'parse_error', 'status_text', 'parse_date', 'external_id',
                  'teams', 'provider', 'external_url')


class ChallengeSerializer(serializers.ModelSerializer):
    provider = serializers.SerializerMethodField()

    def get_provider(self, obj):
        return obj.provider.to_representation()

    class Meta:
        model = Challenge
        fields = ('id', 'title', 'start_date', 'provider')
