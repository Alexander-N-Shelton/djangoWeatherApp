# weather/tasks.py
from django.utils.timezone import now
from django.conf import settings
import requests
from datetime import datetime
import pytz
import dotenv
from .models import WeatherForecast, WeatherCurrent

LATITUDE = 38.02931
LONGITUDE = -78.47668

geocoding_api_key = settings.GEOCODING_API_KEY

local_tz = pytz.timezone("America/New_York")

def get_sunrise_sunset_times(lat, lng, date):
    """Fetch sunrise and sunset times in UTC, then convert to local time with DST handling."""
    base_url = f"https://api.sunrise-sunset.org/json?lat={lat}&lng={lng}&"
    sunrise_sunset_url = f'{base_url}date={date}'    
    
    response_sun = requests.get(sunrise_sunset_url)
    
    if response_sun.status_code != 200:
        print(f"Sunrise-Sunset API Error: {response_sun.status_code}")
        return None, None

    sun_data = response_sun.json()
    utc_sunrise = sun_data["results"]["sunrise"]
    utc_sunset = sun_data["results"]["sunset"]

    def convert_utc_to_local(utc_time_str, date_str):
        """Convert UTC HH:MM:SS AM/PM format to local time with proper DST handling."""
        utc_time = datetime.strptime(utc_time_str, "%I:%M:%S %p")
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")

        # Combine date and time to make full datetime object
        full_utc_time = datetime.combine(date_obj, utc_time.time()).replace(tzinfo=pytz.utc)

        # Convert to New York timezone (Now properly adjusts for DST)
        local_time = full_utc_time.astimezone(local_tz)
        return local_time.time()  

    local_sunrise = convert_utc_to_local(utc_sunrise, date)
    local_sunset = convert_utc_to_local(utc_sunset, date)

    return local_sunrise, local_sunset 

def get_address(lat: float, lon: float) -> dict:
    """Fetches an address based on latitude and longitude"""
    reverse_geocoding_url = f'https://geocode.maps.co/reverse?lat={lat}&lon={lon}&api_key={geocoding_api_key}'
    response = requests.get(reverse_geocoding_url)

    if response.status_code != 200:
        print(f'Error: {response.status_code}')
        return ''
    
    data = response.json()

    # Handle missing address keys safely
    address = data.get('address', {})

    city = (
        address.get('city') or
        address.get('town') or
        address.get('village') or
        address.get('hamlet') or
        address.get('municipality') or
        # As a fallback
        address.get('county')
    )

    state = address.get('state', 'Unknown State')
    country = address.get('country', 'Unknown Country')

    location_data = {
        'city': city if city else 'Unknown City',  # Final fallback
        'state': state,
        'country': country,
    }

    return location_data


def get_coordinates(address:str) -> tuple:
    """Fetches latitude and longitude from address using google's api."""
    forward_geocoding_url = f'https://geocode.maps.co/search?q={address}&api_key={geocoding_api_key}'
    response = requests.get(forward_geocoding_url)

    if response.status_code != 200:
        print(f'Error: {response.status_code}')
        return None, None
    
    data = response.json()
    
    return data[0]['lat'], data[0]['lon']

def update_weather(lat: float, lng: float) -> None:
    """Fetch and store weather forecast with sunrise/sunset times."""
    today = now().date()
    
    WeatherForecast.objects.filter(date__lt=today).delete()

    location_data = get_address(lat, lng)
    if isinstance(location_data, str):
        print(location_data)
        return
    
    city, state, country = location_data['city'], location_data['state'], location_data['country']

    open_meteo_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lng,
        "daily": ["weather_code", "temperature_2m_min", "apparent_temperature_max", 
                    "temperature_2m_max", "rain_sum", "precipitation_probability_mean", 
                    "wind_speed_10m_max", "wind_direction_10m_dominant", 
                    "precipitation_sum", "snowfall_sum", "uv_index_max"],
        "current": ["temperature_2m", "precipitation", "weather_code", "relative_humidity_2m", "wind_speed_10m",
                        "rain", "cloud_cover", "wind_direction_10m", "apparent_temperature", "is_day", "snowfall"],
        "timezone": "auto",
        "wind_speed_unit": "mph",
        "temperature_unit": "fahrenheit",
        "precipitation_unit": "inch"
    }
    response_meteo = requests.get(open_meteo_url, params=params)
    
    if response_meteo.status_code != 200:
        print(f"Open-Meteo API Error: {response_meteo.status_code}")
        return

    open_meteo_data = response_meteo.json()

    current = open_meteo_data["current"]
    location, created = WeatherCurrent.objects.update_or_create(
        latitude=LATITUDE,
        longitude=LONGITUDE,
        defaults={
            "city": city,
            "state": state,
            "country": country,
            "date": datetime.strptime(current["time"], "%Y-%m-%dT%H:%M").date(), 
            "temperature_2m": current["temperature_2m"],
            "precipitation": current["precipitation"],
            "weather_code": current["weather_code"],
            "relative_humidity": current["relative_humidity_2m"],
            "wind_speed": current["wind_speed_10m"],
            "rain": current["rain"],
            "cloud_cover": current["cloud_cover"],
            "wind_direction": current["wind_direction_10m"],
            "apparent_temperature": current["apparent_temperature"],
            "is_day": bool(current["is_day"]),
            "snowfall": current["snowfall"]
        }
    )
    
    forecast_dates = open_meteo_data["daily"]["time"]
    for i in range(len(forecast_dates)):
        date = datetime.strptime(forecast_dates[i], "%Y-%m-%d").date()
        sunrise, sunset = get_sunrise_sunset_times(lat, lng, f'{date}')
        WeatherForecast.objects.update_or_create(
            location=location,
            date = date,
            defaults={
                "weather_code": open_meteo_data["daily"]["weather_code"][i],
                "temperature_2m_min": open_meteo_data["daily"]["temperature_2m_min"][i],
                "apparent_temperature_max": open_meteo_data["daily"]["apparent_temperature_max"][i],
                "temperature_2m_max": open_meteo_data["daily"]["temperature_2m_max"][i],
                "sunrise": sunrise, 
                "sunset": sunset,
                "rain_sum": open_meteo_data["daily"]["rain_sum"][i],
                "wind_speed_10m_max": open_meteo_data["daily"]["wind_speed_10m_max"][i],
                "wind_direction_10m_dominant": open_meteo_data["daily"]["wind_direction_10m_dominant"][i],
                "precipitation_sum": open_meteo_data["daily"]["precipitation_sum"][i],
                "precipitation_probability_mean": open_meteo_data["daily"]["precipitation_probability_mean"][i],
                "snowfall_sum": open_meteo_data["daily"]["snowfall_sum"][i],
                "uv_index_max": open_meteo_data["daily"]["uv_index_max"][i]
            }
        )

    print("Weather data successfully updated with corrected sunrise/sunset times!")
