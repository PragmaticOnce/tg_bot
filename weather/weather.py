import requests

from v1.config import WETHER_API_TOKEN, LOCAL_WEATHER_API_LINK


def get_weather(city, num_of_days=1, lang='ua', output_format='json'):

    """

    :param city:
    :param num_of_days:
    :param lang:
    :param output_format: json, xml, csv, tab
    :return: returns dictionaries current_condition,

    current_condition:
    observation_time

Time of the observation in UTC

Time in UTC hhmm tt format. Examples: 06:45 AM or 11:34 PM

temp_C The temperature in degrees Celsius Integer

temp_F The temperature in degrees Fahrenheit Integer
FeelsLikeC Feels like temperature in degrees Celsius Integer

FeelsLikeF Feels like temperature in degrees Fahrenheit Integer

windspeedMiles Wind speed in miles per hour Integer

windspeedKmph Wind speed in kilometres per hour Integer

winddirDegree Wind direction in degrees Integer

winddir16Point Wind direction in 16-point compass String. Example: N.

weatherCode Weather condition code Integer. See Weather Condition Codes and Icons.

weatherIconUrl URL to weather iconURL

weatherDesc Weather condition description String

precipMM Precipitation in millimetres Integer

precipInches Precipitation in inches. Float

humidity Humidity in percentage Float visibility

Visibility in kilometres Integer

visibilityMiles Visibility in miles. Note:

Integer

pressure

Atmospheric pressure in millibars

Integer

pressureInches

Atmospheric pressure in inches

Float

cloudcover

Cloud cover in percentage

Integer
    """

    weather = requests.get(url=LOCAL_WEATHER_API_LINK,
                           params={'key': WETHER_API_TOKEN,
                                   'q': city,
                                   'lang': lang,
                                   'num_of_days': num_of_days,
                                   'format': output_format}).json()

    return weather['data']


if __name__ == '__main__':
    get_weather('lviv')
