#!/usr/bin/python

import json
import os

import flask
import pyowm

app = flask.Flask(__name__)
#owmapikey = environ.get('baad226337a690b27799026c5f53ffa6')  # i have omitted this line as the os.environ.get is not binding key 
owm = pyowm.OWM(API_key='baad226337a690b27799026c5f53ffa6')


# geting and sending response to dialogflow
@app.route('/webhook', methods=['POST'])
def webhook():
    req = flask.request.get_json()''' --->i am getting http bad request here. and on line 37
    previously request.get_json() was returning null. on doing some google i have understood that it is a version problem of dialogflow APi.
    (they have developed a new version named APIv2 which supports some additional features but the json format of receiving data is different in v1 and v2
    am have problem there only'''

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = flask.make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


# processing the request from dialogflow
def processRequest(req):
    result = req.get("result")
    parameters = result.get("parameters")
    city =str(parameters.get("geo-city"))
    #city = 'Hyderabad'
    observation = owm.weather_at_place(city)
    w = observation.get_weather()
    latlon_res = observation.get_location()
    lat = str(latlon_res.get_lat())
    lon = str(latlon_res.get_lon())

    wind_res = w.get_wind()
    wind_speed = str(wind_res.get('speed'))

    humidity = str(w.get_humidity())

    celsius_result = w.get_temperature('celsius')
    temp_min_celsius = str(celsius_result.get('temp_min'))
    temp_max_celsius = str(celsius_result.get('temp_max'))

    fahrenheit_result = w.get_temperature('fahrenheit')
    temp_min_fahrenheit = str(fahrenheit_result.get('temp_min'))
    temp_max_fahrenheit = str(fahrenheit_result.get('temp_max'))
    speech = "Today the weather in " + city + ": \n" + "Temperature in Celsius:\nMax temp :" + temp_max_celsius + ".\nMin Temp :" + temp_min_celsius + ".\nTemperature in Fahrenheit:\nMax temp :" + temp_max_fahrenheit + ".\nMin Temp :" + temp_min_fahrenheit + ".\nHumidity :" + humidity + ".\nWind Speed :" + wind_speed + "\nLatitude :" + lat + ".\n  Longitude :" + lon
    print(speech)
    return {
        "speech": speech,
        "displayText": speech,
        "source": "dialogflow-weather-by-satheshrgs"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')
