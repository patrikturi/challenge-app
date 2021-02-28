from django.urls import path

from . import views


urlpatterns = [
    path('', views.GetLastChallenge.as_view()),
    path('challenge/<int:pk>/', views.GetChallenge.as_view()),
    path('challenges/', views.ListChallenges.as_view()),
    path('challenges/upcoming/', views.ListUpcomingChallenges.as_view()),
    path('challenges/ended/', views.ListEndedChallenges.as_view()),
]
