from flask import Flask, render_template, request, jsonify, flash
import requests
from geopy.geocoders import Nominatim

app = Flask(__name__)


def get_weather(city):
    loc = Nominatim(user_agent="GetLoc")
    getLoc = loc.geocode(city)
    if getLoc is None:
        return None
    url = f'https://api.open-meteo.com/v1/forecast?latitude={getLoc.latitude}&longitude={getLoc.longitude}&hourly=temperature_2m&forecast_days=1'
    response = requests.get(url)
    response.raise_for_status()
    date = response.json()['hourly']['time']
    time = [single_date.split('T')[-1] for single_date in date]
    cels = response.json()['hourly']['temperature_2m']
    return dict(zip(time, cels))



@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None

    if request.method == 'POST':
        city = request.form['city']
        if city.strip():
            weather_data = get_weather(city)

    return render_template('index.html', weather_data=weather_data)


if __name__ == '__main__':
    app.run(debug=False)
