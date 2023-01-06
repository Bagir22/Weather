from django.urls import re_path, include
from .views import CurrentWeatherAPIView

urlpatterns = [
    re_path(r'^currentWeather/$', CurrentWeatherAPIView.as_view(), name='current_weather'),
]
