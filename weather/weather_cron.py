# weather/weather_cron.py
import os
import django

# Setup Django Environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProjects.settings')
django.setup()

from weather.tasks import update_weather

update_weather()
print("Weather data updated!")