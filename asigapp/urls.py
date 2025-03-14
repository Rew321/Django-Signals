from django.urls import path

from asigapp import views

urlpatterns = [
    path('', views.home, name='index'),
]
