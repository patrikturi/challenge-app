from django.urls import path

from . import views

urlpatterns = [
    path('', views.last_challange, name='last_challange'),
    path('challange/<int:id>/', views.challange_view, name='challange_view')
]
