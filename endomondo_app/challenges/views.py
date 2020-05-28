from django.db.models import Q
from django.http import Http404
from django.utils import timezone
from django.template.response import SimpleTemplateResponse

from challenges.models.challenge import Challenge


def _challenges_to_short_dict(challenges):
    return {'challenges': [ch.to_short_dict() for ch in challenges]}


def _get_challenge_view(challenge_dict):
    if not challenge_dict:
        return {}
    title = challenge_dict['title'] if challenge_dict['title'] else 'Challenge'
    view = {'title': title, 'page_name': 'Home', 'challenge': challenge_dict}
    return view


def last_challenge(request):
    now = timezone.now()
    challenge = Challenge.get_last(now)

    challenge_dict = challenge.to_dict() if challenge else {}

    view = _get_challenge_view(challenge_dict)
    return SimpleTemplateResponse('challenge.html', view)


def challenge_view(request, id):
    try:
        challenge: Challenge = Challenge.objects.get(id=id)
    except Challenge.DoesNotExist:
        raise Http404('Challenge does not exist')

    view = _get_challenge_view(challenge.to_dict())
    return SimpleTemplateResponse('challenge.html', view)


def all_challenges(request):
    challenges = Challenge.objects.order_by('-start_date')
    challenges_view = _challenges_to_short_dict(challenges)
    challenges_view['title'] = 'All Challenges'
    challenges_view['page_name'] = 'All'
    return SimpleTemplateResponse('list_challenges.html', challenges_view)


def upcoming_challenges(request):
    challenges = Challenge.objects.filter( \
        Q(start_date__gt=timezone.now()) | Q(start_date__isnull=True)).order_by('start_date')
    challenges_view = _challenges_to_short_dict(challenges)
    challenges_view['title'] = 'Upcoming Challenges'
    challenges_view['page_name'] = 'Upcoming'
    return SimpleTemplateResponse('list_challenges.html', challenges_view)


def ended_challenges(request):
    challenges = Challenge.objects.filter(end_date__lt=timezone.now()).order_by('-start_date')
    challenges_view = _challenges_to_short_dict(challenges)
    challenges_view['title'] = 'Completed Challenges'
    challenges_view['page_name'] = 'Completed'
    return SimpleTemplateResponse('list_challenges.html', challenges_view)
