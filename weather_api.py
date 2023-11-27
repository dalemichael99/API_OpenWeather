from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_KEY = '00f883f0c9869108ba2c3c8d6b4b64fd'

def kelvin_to_celsius(kelvin_temperature):
    return kelvin_temperature - 273.15

@app.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')

    if not city:
        return jsonify({'error': 'City parameter is required'}), 400

    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}'
    response = requests.get(url)

    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch weather information'}), 500

    data = response.json()

    temperature_kelvin = data['main']['temp']
    temperature_celsius = kelvin_to_celsius(temperature_kelvin)

    weather_info = {
        'city': data['name'],
        'temperature': temperature_celsius,
        'description': data['weather'][0]['description'],
    }

    return jsonify(weather_info)

if __name__ == '__main__':
    app.run(debug=True)