from django.urls import path

from . import views


app_name = 'shortly'

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:slug>', views.resolve, name='resolve'),
]