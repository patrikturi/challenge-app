from django.db.models import Q
from django.utils import timezone
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from challenges.models import Challenge
from challenges.serializers import ChallengeSerializer, ChallengeDetailsSerializer


class GetChallenge(APIView):
    template_name = 'challenge.html'

    def get(self, request, pk, query):
        try:
            challenge = self.get_queryset(pk, query)
        except Challenge.DoesNotExist:
            if query == 'last':
                return Response({})
            else:
                raise NotFound('Challenge does not exist')

        data = {
            'title': challenge.title,
            'page_name': 'Home',
            'challenge': ChallengeDetailsSerializer(challenge).data
        }
        return Response(data)

    def get_queryset(self, pk, query):
        if query == 'last':
            now = timezone.now()
            return Challenge.objects.get_last(now)
        else:
            return Challenge.objects.get(id=pk)


class ListChallenges(APIView):
    template_name = 'list_challenges.html'

    def get(self, request, query):
        queryset = self.get_queryset(query)
        data = {
            'title': 'All Challenges',
            'page_name': 'All',
            'challenges': ChallengeSerializer(queryset, many=True).data
        }
        return Response(data)

    def get_queryset(self, query):
        if query == 'upcoming':
            return Challenge.objects.filter(Q(start_date__gt=timezone.now()) | Q(start_date__isnull=True)).order_by('start_date')
        elif query == 'ended':
            return Challenge.objects.filter(end_date__lt=timezone.now()).order_by('-start_date')
        else:
            return Challenge.objects.order_by('-start_date')
