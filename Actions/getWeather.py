
import requests, json
API_KEY="d13eec5ae3de06c17e40ab5da0a203f9"
def getWeather(city):
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
    URL = BASE_URL + "q=" + city + "&appid=" + API_KEY
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
        main = data['main']
        temperature = main['temp']
        humidity = main['humidity']
        pressure = main['pressure']
        report = data['weather']
        weatherReport=""
        weatherReport+="The temperature in " + city + " is "+str(round(temperature-273.15,1))+" degrees Celsius. "
        weatherReport+="Looks like "+str(report[0]['description'])
        return weatherReport
    else:
        return "Cannot fetch weather details."
