from django.urls import path

from . import views


urlpatterns = [
    path('', views.GetChallenge.as_view(), {'pk': None, 'query': 'last'}),
    path('challenge/<int:pk>/', views.GetChallenge.as_view(), {'query': 'id'}),
    path('challenges/', views.ListChallenges.as_view(), {'query': 'all'}),
    path('challenges/upcoming/', views.ListChallenges.as_view(), {'query': 'upcoming'}),
    path('challenges/ended/', views.ListChallenges.as_view(), {'query': 'ended'}),
]
