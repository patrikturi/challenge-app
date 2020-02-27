from django.template.response import SimpleTemplateResponse

from challanges.models.challange import Challange


def last_challange(request):
    challange: Challange = Challange.objects.all()[1]

    return SimpleTemplateResponse('challange.html', challange.to_dict())


def challange_view(request, id):
    challange: Challange = Challange.objects.get(id=id)
    return SimpleTemplateResponse('challange.html', challange.to_dict())
