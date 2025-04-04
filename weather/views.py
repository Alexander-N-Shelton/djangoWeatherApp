# weather/views.py
from django.shortcuts import render, redirect
from .forms import LocationForm
from .tasks import update_weather, get_coordinates
from .models import WeatherCurrent, WeatherForecast

def convert_measurement_system(value, unit, unit_type):
    """Converts between Standard and Metric for temperature, measurement, and speed."""
    conversion = {
        'temp': lambda v: round((v - 32) * 5 / 9, 1),   # °F -> °C
        'measurement': lambda v: round(v * 25.4, 1),    # inches -> mm
        'speed': lambda v: round(v * 1.609344, 1),      # mp/h -> km/h
    }
    return conversion[unit_type](value) if unit == 'Metric' else value

def weather_view(request):
    form = LocationForm()
    forecast = WeatherForecast.objects.select_related('location').all()
    current_weather = WeatherCurrent.objects.first()

    current_units = request.session.get("current_units", "Standard")

    if request.method == "POST" and "toggle_units" in request.POST:
        request.session['current_units'] = 'Metric' if current_units == 'Standard' else 'Standard'
        return redirect('weather')

    if current_weather:
        current_weather.temperature_2m = convert_measurement_system(current_weather.temperature_2m, current_units, 'temp')
        current_weather.apparent_temperature = convert_measurement_system(current_weather.apparent_temperature, current_units,'temp')
        current_weather.precipitation = convert_measurement_system(current_weather.precipitation, current_units,'measurement')
        current_weather.rain = convert_measurement_system(current_weather.rain, current_units,'measurement')
        current_weather.snowfall = convert_measurement_system(current_weather.snowfall, current_units,'measurement')
        current_weather.wind_speed = convert_measurement_system(current_weather.wind_speed, current_units,'speed')


    for day in forecast:
        day.temperature_2m_max = convert_measurement_system(day.temperature_2m_max, current_units, 'temp')
        day.temperature_2m_min = convert_measurement_system(day.temperature_2m_min, current_units, 'temp')
        day.apparent_temperature_max = convert_measurement_system(day.apparent_temperature_max, current_units, 'temp')
        day.precipitation_sum = convert_measurement_system(day.precipitation_sum, current_units, 'measurement')
        day.rain_sum = convert_measurement_system(day.rain_sum, current_units, 'measurement')
        day.snowfall_sum = convert_measurement_system(day.snowfall_sum, current_units, 'measurement')
        day.wind_speed_10m_max = convert_measurement_system(day.wind_speed_10m_max, current_units, 'speed')

    if request.method == "POST":
        form = LocationForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            country = form.cleaned_data['country']

            print(f"User entered location: {city}, {state}, {country}") # Print for troubleshooting issues

            # Get Coordinates from Google API
            coordinates = get_coordinates(f"{city}, {state}, {country}")
            print(f"Coordinates received: {coordinates}") # Print for troubleshooting issues

            if isinstance(coordinates, str): # If API returned an error
                return render(
                    request, "weather/weather_view.html", {
                        "form": form,
                        "error": coordinates,
                        "forecast": forecast,
                    }
                )

            lat, lng = coordinates

            update_weather(lat, lng)

            return redirect("weather")

    return render(
        request, 'weather/weather_view.html', {
            'current': current_weather,
            'forecast': forecast,
            'form': form,
            'current_units': current_units,
        }
    )