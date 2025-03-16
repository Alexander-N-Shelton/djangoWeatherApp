# weather/tasks.py
from celery import shared_task
import requests
from datetime import datetime
import pytz
import dotenv
from .models import WeatherForecast, WeatherCurrent

LATITUDE = 38.02931
LONGITUDE = -78.47668

google_api_key = dotenv.get_key('.env', 'GOOGLE_API_KEY')

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

def get_address(lat, lng) -> dict:
    """Fetches an address based on latitude and longitude"""
    google_geocoding_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "latlng": f"{lat},{lng}",
        "key": google_api_key,
    }

    response = requests.get(google_geocoding_url, params)
    data = response.json()

    if data['status'] != 'OK':
        return f'Error: {data['status']}'
    
    components = data['results'][0]['address_components']
    location_data = {
        'city': None,
        'state': None,
        'country': None,
    }
    for component in components:
        if "locality" in component['types']:
            location_data['city'] = component['short_name']
        elif "administrative_area_level_1" in component['types']:
            location_data['state'] = component['short_name']
        elif "country" in component['types']:
            location_data['country'] = component['short_name']

    return location_data

def get_coordinates(address: str) -> tuple:
    """Fetches latitude and longitude from address using google's api."""
    google_geocoding_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": address,
        "key": google_api_key,
    }
    
    response = requests.get(google_geocoding_url, params)
    data = response.json()

    if data['status'] != "OK":
        return f'Error: {data['status']}'
    
    location = data['results'][0]['geometry']['location']
    return location['lat'], location['lng']

@shared_task
def update_weather(lat: float, lng: float) -> None:
    """Fetch and store weather forecast with sunrise/sunset times."""
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
