from datetime import datetime

from django.db.models import Q
from django.template.response import SimpleTemplateResponse

from challanges.models.challange import Challange


def _challanges_to_short_dict(challanges):
    return {'challanges': [ch.to_short_dict() for ch in challanges]}


def last_challange(request):
    now = datetime.now()
    active_challanges = Challange.objects.filter( \
        Q(start_date__lt=now, end_date__gt=now) | Q(start_date__isnull=True)) \
        .order_by('-start_date')
    
    if len(active_challanges) > 0:
        challange = active_challanges[0]
    else:
        challanges_ended = Challange.objects.filter(end_date__lt=datetime.now()).order_by('-end_date')
        if len(challanges_ended) > 0:
            challange = challanges_ended[0]
        else:
            challange = None

    challange_dict = challange.to_dict() if challange else {}
    return SimpleTemplateResponse('challange.html', challange_dict)


def challange_view(request, id):
    challange: Challange = Challange.objects.get(id=id)
    return SimpleTemplateResponse('challange.html', challange.to_dict())


def all_challanges(request):
    challanges = Challange.objects.all().order_by('-start_date')
    challanges_view = _challanges_to_short_dict(challanges)
    challanges_view['title'] = 'All Challanges'
    return SimpleTemplateResponse('list_challanges.html', challanges_view)


def upcoming_challanges(request):
    challanges = Challange.objects.filter( \
        Q(start_date__gt=datetime.now()) | Q(start_date__isnull=True)).order_by('start_date')
    challanges_view = _challanges_to_short_dict(challanges)
    challanges_view['title'] = 'Upcoming Challanges'
    return SimpleTemplateResponse('list_challanges.html', challanges_view)


def ended_challanges(request):
    challanges = Challange.objects.filter(end_date__lt=datetime.now()).order_by('-start_date')
    challanges_view = _challanges_to_short_dict(challanges)
    challanges_view['title'] = 'Completed Challanges'
    return SimpleTemplateResponse('list_challanges.html', challanges_view)
