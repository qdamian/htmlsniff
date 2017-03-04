"""
A tiny service that helps you plan your day based on the weather forecast
"""
import json
import requests
import bottle

TIP_BY_WEATHER = {
    'sunny': 'go hiking',
    'rainy': 'better stay home',
}


@bottle.get('/recommendation')
def recommendation():
    response = requests.get('http://127.0.0.1:9999/forecast')
    response.raise_for_status()
    json_data = json.loads(response.text)
    forecast = json_data['weather']
    return TIP_BY_WEATHER[forecast]


bottle.run(host='localhost', port=8080)
