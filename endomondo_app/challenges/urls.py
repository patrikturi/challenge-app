from django.urls import path

from . import views

urlpatterns = [
    path('', views.last_challenge),
    path('challenge/<int:id>/', views.challenge_view),
    path('challenges/', views.all_challenges),
    path('challenges/upcoming/', views.upcoming_challenges),
    path('challenges/ended/', views.ended_challenges),
]
