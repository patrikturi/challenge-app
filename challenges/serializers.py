from django.db.models import Prefetch, Q
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from .models import Challenge, Competitor, Stats, Team, ExternalProfile


class CompetitorSerializer(serializers.ModelSerializer):
    external_id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    score = serializers.SerializerMethodField()
    external_url = serializers.SerializerMethodField()

    def _get_profile(self, obj):
        profiles = obj.external_profiles.all()
        return profiles[0] if len(profiles) > 0 else None

    def get_name(self, obj):
        p = self._get_profile(obj)
        return obj.get_name(p.name if p else None)

    def get_external_id(self, obj):
        p = self._get_profile(obj)
        return str(p.external_id) if p else ''

    def get_score(self, obj):
        try:
            return self.context['provider'].get_score(obj.stats)
        except Stats.DoesNotExist:
            return 0

    def get_external_url(self, obj):
        return self.context['provider'].get_competitor_url(self.get_external_id(obj))

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
        return self.context['provider'].get_team_score(obj.competitors)

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
        provider_type =  obj.provider.get_type()
        teams = Team.objects.filter(challenge=obj).prefetch_related('competitors') \
                .prefetch_related(Prefetch('competitors__stats', queryset=Stats.objects.filter(Q(challenge=obj) | Q(challenge=None)))) \
                .prefetch_related(Prefetch('competitors__external_profiles', queryset=ExternalProfile.objects.filter(kind=provider_type)))
        return TeamSerializer(teams, context={'provider': obj.provider}, many=True).data

    def get_provider(self, obj):
        return obj.provider.to_representation()

    class Meta:
        model = Challenge
        fields = ('id', 'title', 'start_date', 'end_date', 'parse_error', 'status_text', 'parse_date', 'external_id',
                  'teams', 'provider', 'score_units', 'external_url')


class ChallengeSerializer(serializers.ModelSerializer):
    provider = serializers.SerializerMethodField()

    def get_provider(self, obj):
        return obj.provider.to_representation()

    class Meta:
        model = Challenge
        fields = ('id', 'title', 'start_date', 'provider')
