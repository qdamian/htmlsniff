"""
A suite of functional tests for the activity recommendation service.
"""
import requests


def test_recommends_to_go_hiking_if_the_weather_is_sunny():
    _given_weather_is('sunny')
    response = requests.get('http://127.0.0.1:8080/recommendation')
    response.raise_for_status()
    assert response.text == 'go hiking'


def test_recommends_to_stay_home_if_the_weather_is_rainy():
    _given_weather_is('rainy')
    response = requests.get('http://127.0.0.1:8080/recommendation')
    response.raise_for_status()
    assert response.text == 'better stay home'


def _given_weather_is(weather):
    response = requests.put(
        'http://127.0.0.1:9999/response', json={'weather': weather})
    response.raise_for_status()
