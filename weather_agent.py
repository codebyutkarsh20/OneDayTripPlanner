import os
import requests
from dotenv import load_dotenv
load_dotenv()
weather_api_key = os.getenv("WEATHER_API_KEY")

def fetch_weather(city, date):
    """Fetch weather information for a specified city and date."""
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={weather_api_key}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        weather_data = response.json()
        return weather_data
    except requests.exceptions.RequestException as e:
        print(f"Weather API error: {e}")
        return None

