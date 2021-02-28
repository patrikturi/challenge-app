from django.db.models import Q
from django.utils import timezone
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from challenges.models.challenge import Challenge
from challenges.serializers import ChallengeSerializer, ChallengeDetailsSerializer


class GetLastChallenge(APIView):
    template_name = 'challenge.html'

    def get(self, request):
        now = timezone.now()
        challenge = Challenge.get_last(now)

        if challenge is None:
            return {}

        data = {
            'title': challenge.title,
            'page_name': 'Home',
            'challenge': ChallengeDetailsSerializer(challenge).data
        }
        return Response(data)


class GetChallenge(APIView):
    template_name = 'challenge.html'

    def get(self, request, pk):
        try:
            challenge = Challenge.objects.get(id=pk)
        except Challenge.DoesNotExist:
            raise NotFound('Challenge does not exist')

        data = {
            'title': challenge.title,
            'page_name': 'Home',
            'challenge': ChallengeDetailsSerializer(challenge).data
        }
        return Response(data)


class ListChallenges(APIView):
    template_name = 'list_challenges.html'

    def get(self, request):
        queryset = Challenge.objects.order_by('-start_date')
        data = {
            'title': 'All Challenges',
            'page_name': 'All',
            'challenges': ChallengeSerializer(queryset, many=True).data
        }
        return Response(data)


class ListUpcomingChallenges(APIView):
    template_name = 'list_challenges.html'

    def get(self, request):
        queryset = Challenge.objects.filter( \
        Q(start_date__gt=timezone.now()) | Q(start_date__isnull=True)).order_by('start_date')
        data = {
            'title': 'Upcoming Challenges',
            'page_name': 'Upcoming',
            'challenges': ChallengeSerializer(queryset, many=True).data
        }
        return Response(data)


class ListEndedChallenges(APIView):
    template_name = 'list_challenges.html'

    def get(self, request):
        queryset = Challenge.objects.filter(end_date__lt=timezone.now()).order_by('-start_date')
        data = {
            'title': 'Completed Challenges',
            'page_name': 'Completed',
            'challenges': ChallengeSerializer(queryset, many=True).data
        }
        return Response(data)
