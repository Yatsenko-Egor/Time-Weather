import requests
from decoding_of_weather_parameters import transcript_of_weather_description, decoding_wind_direction


def get_weather(city, current=True):
    lat, lon = search_city(city)
    api_server = 'https://api.weather.yandex.ru/v2/forecast?'
    search_params = {
        "lat": lat,
        "lon": lon,
        "lang": "ru_RU",
        "limit": "3",
        "hours": "true",
        "extra": "false", }
    header = {"X-Yandex-API-Key": "60ea7209-84e4-46df-b368-fc8ba8712777"}
    response = requests.get(api_server, params=search_params, headers=header)
    if not response:
        return response.reason
    else:
        if current:
            weather = get_current_weather(response.json())
        else:
            weather = get_weather_forecast(response.json())
    return weather


def get_current_weather(information):
    weather = {}
    information = information["fact"]
    icon = information["icon"]
    weather["Icon"] = f"https://yastatic.net/weather/i/icons/blueye/color/svg/{icon}.svg"
    weather['condition'] = transcript_of_weather_description[information["condition"]].capitalize()
    weather["Температура"] = str(information["temp"]) + " °C"
    weather["Ощущается как"] = str(information["feels_like"]) + " °C"
    weather["Скорость ветра"] = str(information["wind_speed"]) + " м/с"
    weather['Направление ветра'] = decoding_wind_direction[information["wind_dir"]]
    weather['Давление'] = str(information["pressure_mm"]) + ' мм рт. ст.'
    weather['Влажность воздуха'] = str(information['humidity']) + '%'
    return weather


def get_weather_forecast(information):
    weather = {}
    for day in information['forecasts']:
        forecast_for_day = {}
        forecast_for_day["forecast"] = {}
        for hour in day["hours"]:
            forecast_for_hour = {}
            icon = hour["icon"]
            forecast_for_hour["icon"] = f"https://yastatic.net/weather/i/icons/blueye/color/svg/{icon}.svg"
            forecast_for_hour["condition"] = transcript_of_weather_description[hour['condition']].capitalize()
            forecast_for_hour["Температура"] = str(hour['temp']) + "°C"
            forecast_for_hour["Ощущается как"] = str(hour['feels_like']) + "°C"
            forecast_for_hour["Скорость ветра"] = str(hour['wind_speed']) + " м/с"
            forecast_for_hour['Направление ветра'] = decoding_wind_direction[hour["wind_dir"]]
            forecast_for_hour['Давление'] = str(hour["pressure_mm"]) + ' мм рт. ст.'
            forecast_for_hour['Влажность воздуха'] = str(hour['humidity']) + '%'
            forecast_for_day["forecast"][int(hour["hour"])] = forecast_for_hour
        forecast_for_day["max_hour"] = len(day["hours"])
        date = '.'.join(day["date"].split('-')[::-1])
        weather[date] = forecast_for_day
    return weather


def search_city(name):
    information = geocode(name)
    lat, lon = information["Point"]["pos"].split()[::-1]
    return lat, lon


def geocode(address):
    geocoder_request = f"http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": address,
        "format": "json"}
    response = requests.get(geocoder_request, params=geocoder_params)
    if response:
        json_response = response.json()
    else:
        raise RuntimeError(
            f"""Ошибка выполнения запроса:
            {geocoder_request}
            Http статус: {response.status_code} ({response.reason})""")
    features = json_response["response"]["GeoObjectCollection"]["featureMember"]
    if features:
        return features[0]["GeoObject"]
    else:
        return None
