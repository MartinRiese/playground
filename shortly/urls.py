from django.urls import path

from shortly import views
from shortly.views import ShortlyView


app_name = 'shortly'

urlpatterns = [
    path('', ShortlyView.as_view(), name='index'),
    path('<str:slug>', views.resolve, name='resolve'),
]