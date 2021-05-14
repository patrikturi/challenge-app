from django.urls import path

from . import api


urlpatterns = [
    path('token-exchange/', api.ExchangeToken.as_view()),
]
