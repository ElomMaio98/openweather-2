import os
import requests
def get_weather(lat,long):
    key = os.getenv('OPEN_WEATHER_API_KEY')
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={long}&appid={key}&units=metric'
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Error fetching weather data: {response.status_code} - {response.text}")
    else:
        data = response.json()
        return {
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'description': data['weather'][0]['description']
        }
    
