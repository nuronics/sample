#!/usr/bin/python 

from flask import Flask,request,make_response
import os,json
import pyowm
import os

app = Flask(__name__)
owmapikey=os.environ.get('4880f488e7141442da2967d2d90954f6') #or provide your key here
owm = pyowm.OWM(owmapikey)

#geting and sending response to dialogflow
@app.route('/webhook',methods=['POST'])
def webhook():
    try:               
            req = request.get_json(force=True)
            print("Request:")
            print(json.dumps(req, indent=4))
            res = processRequest(req)
            res = json.dumps(res, indent=4)
            print(res)
            r = make_response(res)
            r.headers['Content-Type'] = 'application/json'
            
    except Exception as e:
        print(e)
    return r
#processing the request from dialogflow
'''def processRequest(req):
    try:
        print("inside process request")
        result = req.get("result") 
        parameters = result.get("parameters")
        city = parameters.get("geo-city")
        #city = 'Hyderabad'
        observation = owm.weather_at_place(city)
        w = observation.get_weather()
        latlon_res = observation.get_location()
        lat=str(latlon_res.get_lat())
        lon=str(latlon_res.get_lon())
        wind_res=w.get_wind()
        wind_speed=str(wind_res.get('speed'))
        humidity=str(w.get_humidity())
        celsius_result=w.get_temperature('celsius')
        temp_min_celsius=str(celsius_result.get('temp_min'))
        temp_max_celsius=str(celsius_result.get('temp_max'))
        fahrenheit_result=w.get_temperature('fahrenheit')
        temp_min_fahrenheit=str(fahrenheit_result.get('temp_min'))
        temp_max_fahrenheit=str(fahrenheit_result.get('temp_max'))
        speech = "Today the weather in " + city + ": \n" + "Temperature in Celsius:\nMax temp :"+temp_max_celsius+".\nMin Temp :"+temp_min_celsius+".\nTemperature in Fahrenheit:\nMax temp :"+temp_max_fahrenheit+".\nMin Temp :"+temp_min_fahrenheit+".\nHumidity :"+humidity+".\nWind Speed :"+wind_speed+"\nLatitude :"+lat+".\n  Longitude :"+lon
        print(speech)
        return {
        "speech": speech,
        "displayText": speech,
        "source": "dialogflow-weather-by-satheshrgs"
        }
    except Exception as e:
                         print(e)
                         '''
def processRequest(req):
    try:
        print("b4 req.get")
        if req.get("result").get("action")=="yahooWeatherForecast":
            print("after req.get")
            baseurl = "https://query.yahooapis.com/v1/public/yql?"
            yql_query = makeYqlQuery(req)
            if yql_query is None:
                return {}
            yql_url = baseurl + urlencode({'q': yql_query}) + "&format=json"
            result = urlopen(yql_url).read()
            data = json.loads(result)
            res = makeWebhookResult(data)
    except Exception as e :
                            print(e)

def makeYqlQuery(req):
    result = req.get("result")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    if city is None:
        return None

    return "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='" + city + "')"


def makeWebhookResult(data):
    query = data.get('query')
    if query is None:
        return {}

    result = query.get('results')
    if result is None:
        return {}

    channel = result.get('channel')
    if channel is None:
        return {}

    item = channel.get('item')
    location = channel.get('location')
    units = channel.get('units')
    if (location is None) or (item is None) or (units is None):
        return {}

    condition = item.get('condition')
    if condition is None:
        return {}

    # print(json.dumps(item, indent=4))

    speech = "Today in " + location.get('city') + ": " + condition.get('text') + \
             ", the temperature is " + condition.get('temp') + " " + units.get('temperature')

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
        }

    
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port)
