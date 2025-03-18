# weather/weather_cron.py
import os
import sys
import django

# Set the Django project base directory
sys.path.append('/home/djangoWeatherWebApp/djangoProjects')  # Adjust this path!

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProjects.settings')  # Update 'weather' if different

# Initialize Django
django.setup()

# Import and run the update_weather function
from weather.tasks import update_weather
from weather.models import WeatherCurrent

current = WeatherCurrent.objects.first()

lat, long = current.latitude, current.longitude

update_weather()
