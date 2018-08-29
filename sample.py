#!/usr/bin/python

import json
import os

import flask
import requests

app = flask.Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = flask.request.get_json()
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
    date =str(parameters.get("date"))
    #city = 'Hyderabad'
    api_address ='http://api.worldweatheronline.com/premium/v1/weather.ashx?key=f53dbc7d463e4310b6865407181308&tp=3&format=json&q='

    url = api_address+city+"&date="+date
    json_data = requests.get(url).json()
    weatherDesc = getweatherDesc(json_data)  
    
   ''' w = observation.get_weather()
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
    temp_max_fahrenheit = str(fahrenheit_result.get('temp_max'))'''
    speech = "Today the weather in " + city + ": \n" +weatherDesc
    print(speech)
    return {
        "speech": speech,
        "displayText": speech,
        "source": "dialogflow-weather-by-satheshrgs"
    }

def getweatherDesc(dict) :
    ass = json_data
    weather = ass.get('data').get('current_condition')
    weatherD = str(weather)
    print(type(weatherD))
    weatherD = ast.literal_eval(str(weather[0]))
    print(ast.literal_eval(str(weatherD.get('weatherDesc')[0])).get('value'))
    return


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
app.run(debug=False, port=port, host='0.0.0.0')
