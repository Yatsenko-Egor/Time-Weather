import requests


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
            weather = response.json()
        else:
            weather = get_weather_forecast(response.json())
    return weather


def get_weather_forecast(information):
    pass


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
