from flask import Flask, render_template
from get_weather import get_weather

app = Flask(__name__)


@app.route('/current_weather/<city>')
def show_current_weather(city):
    weather_params = get_weather(city)
    params = {}
    params["city"] = city
    return render_template("current_weather_page.html", weather_params=weather_params, **params)


@app.route('/weather_forecast/<city>')
def show_weather_forecast(city):
    weather_forecast = get_weather(city, False)
    params = {}
    params["city"] = city
    return render_template("weather_forecast_page.html", weather_forecast=weather_forecast, **params)




if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')