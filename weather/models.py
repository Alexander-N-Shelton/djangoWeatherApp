# weather/models.py
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class WeatherCurrent(models.Model):
    latitude = models.FloatField(validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)])
    longitude = models.FloatField(validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)])
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    current_units = models.CharField(max_length=10)
    date = models.DateField()
    temperature_2m = models.FloatField()
    precipitation = models.FloatField()
    weather_code = models.IntegerField()
    relative_humidity = models.IntegerField()
    wind_speed = models.FloatField()
    rain = models.FloatField()
    cloud_cover = models.IntegerField()
    wind_direction = models.IntegerField()
    apparent_temperature = models.FloatField()
    is_day = models.BooleanField()
    snowfall = models.FloatField()

    def __str__(self):
        return f"Weather at {self.city}, {self.state}, {self.country} on {self.date}"


class WeatherForecast(models.Model):
    location = models.ForeignKey(WeatherCurrent, on_delete=models.CASCADE)
    current_units = models.CharField(max_length=10)
    date = models.DateField()
    weather_code = models.IntegerField()
    temperature_2m_min = models.FloatField()
    apparent_temperature_max = models.FloatField()
    temperature_2m_max = models.FloatField()
    sunrise = models.TimeField()
    sunset = models.TimeField()
    rain_sum = models.FloatField()
    wind_speed_10m_max = models.FloatField()
    wind_direction_10m_dominant = models.IntegerField()
    precipitation_sum = models.FloatField() 
    precipitation_probability_mean = models.IntegerField()
    snowfall_sum = models.FloatField()
    uv_index_max = models.FloatField()

    def __str__(self):
        return f"Forecast for {self.location.city}, {self.location.state} on {self.date}: High {self.temperature_2m_max}°F, Low {self.temperature_2m_min}°F"