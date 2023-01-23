import requests
import os
import ipinfo

from dotenv import load_dotenv
from users.models import UserFavourites

base_url = 'http://api.openweathermap.org/data/2.5/'

load_dotenv()
owmAPI = os.getenv('owmAPI')
city = None

base_weather_data = []
cities = ['New York', 'London', 'Moscow', 'Dubai', 'Tokyo']


def get_base_weather():
    for city in cities:
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={owmAPI}'
        city_weather = requests.get(
            url.format(city)).json()
        base_weather = {
            'city_name': city,
            'city_country': city_weather['sys']['country'],
            'temperature': city_weather['main']['temp'],
            'min_temperature': city_weather['main']['temp_min'],
            'max_temperature': city_weather['main']['temp_max'],
            'visibility': city_weather['visibility'],
            'wind_speed': city_weather['wind']['speed'],
            'clouds': city_weather['clouds']['all'],
            'description': city_weather['weather'][0]['description'],
        }

        base_weather_data.append(base_weather)

    return base_weather_data


def get_user_weather(self, request):
    ip = _get_client_ip(request)
    lat, lon = _get_user_location(ip)

    if lat is not None and lon is not None:
        url = base_url + f'weather?lat={lat}&lon={lon}&units=metric&appid={owmAPI}'
        user_city = requests.get(url).json()
        user_city_weather = _get_weather(user_city)

        return user_city_weather


def get_search_weather(query):
    try:
        url = f'http://api.openweathermap.org/data/2.5/weather?q={query}&units=metric&appid={owmAPI}'
        user_city = requests.get(url).json()
        search_city_weather = _get_weather(user_city)

        return search_city_weather
    except:
        return None


def get_user_favourites_weather(self, User):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid='
    url += owmAPI
    base_weather_data = []
    cities = _get_favourite_cites(User)
    if cities is not None:
        for city in cities:
            city_weather = requests.get(
                url.format(city)).json()
            base_weather = _get_weather(city_weather)
            base_weather_data.append(base_weather)

        return base_weather_data


def get_search_history(search_cities):
    search_cities_weather = []
    for city in search_cities:
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city[0]}&units=metric&appid={owmAPI}'
        city_weather = requests.get(
            url.format(city)).json()
        search_city = {
            'city_name': city,
            'city_country': city_weather['sys']['country'],
            'temperature': city_weather['main']['temp'],
            'min_temperature': city_weather['main']['temp_min'],
            'max_temperature': city_weather['main']['temp_max'],
            'visibility': city_weather['visibility'],
            'wind_speed': city_weather['wind']['speed'],
            'clouds': city_weather['clouds']['all'],
            'description': city_weather['weather'][0]['description'],
        }

        search_cities_weather.append(search_city)

    return search_cities_weather


def _get_weather(city):
    city_weather = {
        'city_name': city['name'],
        'city_country': city['sys']['country'],
        'temperature': city['main']['temp'],
        'min_temperature': city['main']['temp_min'],
        'max_temperature': city['main']['temp_max'],
        'visibility': city['visibility'],
        'wind_speed': city['wind']['speed'],
        'clouds': city['clouds']['all'],
        'description': city['weather'][0]['description'],
    }

    return city_weather


def _get_favourite_cites(User):
    cities = []
    cities_instance = UserFavourites.objects.all().filter(user_id=User.pk)
    for city in cities_instance:
        cities.append(city.city)
    if len(cities) != 0:
        return cities
    else:
        return None


def _get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def _get_user_location(ip):
    handler = ipinfo.getHandler(access_token=os.getenv('ipinfo_token'))
    #details = handler.getDetails(ip)
    details = handler.getDetails('146.70.81.130')
    latitude, longitude = details.latitude, details.longitude
    return latitude, longitude
