from flask import Flask, render_template
import sqlite3
from get_weather import get_weather

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    rus = []
    ext = []
    ext_d = {}
    param = {}
    param['title'] = 'Time'
    con = sqlite3.connect("time_db.sql")
    cur = con.cursor()
    result = cur.execute(f'''SELECT city FROM cities''').fetchall()
    param['result'] = result
    for cities in result:
        for city in cities:
            city = city.split('(')
            if len(city) == 1:
                rus.append(city[0])
            else:
                ext.append(city[0])
                ext_d[city[0]] = city[1][0:-1]
    rus.reverse()
    ext = sorted(ext)
    param['num_rus'] = len(rus)
    param['num_ext'] = len(ext)
    param['rus'] = rus
    param['ext'] = ext
    param['ext_d'] = ext_d
    return render_template('main.html', **param)


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


@app.errorhandler(500)
def server_error(error):
    params = {}
    params["text"] = "Извините, но такой город не найден"
    return render_template("error_file.html", **params)


@app.errorhandler(404)
def error_not_found(error):
    params = {}
    params["text"] = "Извините, такая страница не найдена"
    return render_template("error_file.html", **params)


if name == 'main':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)