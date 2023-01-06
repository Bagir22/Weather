from rest_framework.views import APIView
from rest_framework.response import Response

from .backends import get_base_weather, get_user_weather, get_user_favourites_weather, get_search_weather, get_search_history
from users.models import UserSearchHistory

import os
from dotenv import load_dotenv

base_url = 'http://api.openweathermap.org/data/2.5/'

load_dotenv()
owmAPI = os.getenv('owmAPI')


class CurrentWeatherAPIView(APIView):
    def get(self, request):
        data = {
            "base_weather": [],
            "user_weather": [],
            "search_weather": [],
            "user_favourites_weather": [],
            "search_history_weather": [],
        }

        data["base_weather"].append(get_base_weather())
        data["user_weather"].append(get_user_weather(self, request))

        # Поиск
        if request.GET.get("q", None) is not None:
            query = request.GET.get("q")
            data["search_weather"].append(get_search_weather(query))
            if data["search_weather"][0] is not None and request.user.is_authenticated:
                if not UserSearchHistory.objects.filter(city=query, user=request.user):
                    UserSearchHistory.objects.create(city=query, user=request.user)

        # Избранные города
        if request.user.is_authenticated:
            data["user_favourites_weather"].append(get_user_favourites_weather(self, request.user))

        # История поиска
        if request.user.is_authenticated:
            queryset = UserSearchHistory.objects.filter(user=request.user).values_list('city')
            if queryset:
                data["search_history_weather"].append(get_search_history(queryset))

        return Response(data)
