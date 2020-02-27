from django.urls import path

from . import views

urlpatterns = [
    path('', views.last_challange),
    path('challange/<int:id>/', views.challange_view),
    path('challanges/', views.all_challanges),
    path('challanges/upcoming/', views.upcoming_challanges),
    path('challanges/ended/', views.ended_challanges),
]
