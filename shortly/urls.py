from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from shortly import views
from shortly.views import ShortlyView

app_name = 'shortly'

urlpatterns = [
                  path('', ShortlyView.as_view(), name='index'),
                  path('<str:slug>', views.resolve, name='resolve'),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
