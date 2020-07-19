import requests
from v1.config import SEARCH_API_LINK, WETHER_API_TOKEN, LOCAL_WEATHER_API_LINK


def search_city(city):
    try:
        weather = requests.get(SEARCH_API_LINK, params={'key': WETHER_API_TOKEN,
                                                        'query': city,
                                                        'num_of_results': 8,
                                                        'format': 'json'}).json()
        citys = []
        countrys = []
        for place in weather['search_api']['result']:
            for city in place['areaName']:
                citys.append(city['value'])

        for place in weather['search_api']['result']:
            for city in place['country']:
                countrys.append(city['value'])

        result = []
        for i in range(len(citys)):
            result.append(f"{citys[i]}({countrys[i]})")

        return result
    except KeyError:
        return '❗❗️❗️There are no cities matching this query❗️❗️❗️'

def get_weather(city):
    try:
        weather = requests.get(LOCAL_WEATHER_API_LINK,params={'key': WETHER_API_TOKEN,
                                                              'q': city,
                                                              'lang': 'ua',
                                                              'format': 'json',
                                                              'num_of_days': 1
                                                              }).json()
        return weather
    except KeyError:
        return 1
