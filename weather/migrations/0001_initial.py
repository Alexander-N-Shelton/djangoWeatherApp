# Generated by Django 5.1.3 on 2025-03-15 16:31

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="WeatherCurrent",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "latitude",
                    models.FloatField(
                        validators=[
                            django.core.validators.MinValueValidator(-90.0),
                            django.core.validators.MaxValueValidator(90.0),
                        ]
                    ),
                ),
                (
                    "longitude",
                    models.FloatField(
                        validators=[
                            django.core.validators.MinValueValidator(-180.0),
                            django.core.validators.MaxValueValidator(180.0),
                        ]
                    ),
                ),
                ("city", models.CharField(blank=True, max_length=100, null=True)),
                ("state", models.CharField(blank=True, max_length=100, null=True)),
                ("country", models.CharField(blank=True, max_length=100, null=True)),
                ("current_units", models.CharField(max_length=10)),
                ("date", models.DateField()),
                ("temperature_2m", models.FloatField()),
                ("precipitation", models.FloatField()),
                ("weather_code", models.IntegerField()),
                ("relative_humidity", models.IntegerField()),
                ("wind_speed", models.FloatField()),
                ("rain", models.FloatField()),
                ("cloud_cover", models.IntegerField()),
                ("wind_direction", models.IntegerField()),
                ("apparent_temperature", models.FloatField()),
                ("is_day", models.BooleanField()),
                ("snowfall", models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name="WeatherForecast",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("current_units", models.CharField(max_length=10)),
                ("date", models.DateField()),
                ("weather_code", models.IntegerField()),
                ("temperature_2m_min", models.FloatField()),
                ("apparent_temperature_max", models.FloatField()),
                ("temperature_2m_max", models.FloatField()),
                ("sunrise", models.TimeField()),
                ("sunset", models.TimeField()),
                ("rain_sum", models.FloatField()),
                ("wind_speed_10m_max", models.FloatField()),
                ("wind_direction_10m_dominant", models.IntegerField()),
                ("precipitation_sum", models.FloatField()),
                ("precipitation_probability_max", models.IntegerField()),
                ("snowfall_sum", models.FloatField()),
                ("uv_index_max", models.FloatField()),
                (
                    "location",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="weather.weathercurrent",
                    ),
                ),
            ],
        ),
    ]
