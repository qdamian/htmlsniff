"""
A configurable fake weather service to test our recommendations web app
"""
import bottle

responses = []


@bottle.put('/response')
def response():
    weather = bottle.request.json['weather']
    responses.append(weather)


@bottle.get('/forecast')
def forecast():
    return {"weather": responses.pop()}


bottle.run(host='localhost', port=9999)
