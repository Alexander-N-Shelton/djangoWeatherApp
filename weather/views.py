# weather/views.py
from django.shortcuts import render, redirect
from django.conf import settings
from .forms import LocationForm
from .tasks import update_weather, get_coordinates
from .models import WeatherCurrent, WeatherForecast

def weather_view(request):
    form = LocationForm()
    forecast = WeatherForecast.objects.select_related('location').all()
    current_weather = WeatherCurrent.objects.first()
    
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

            # Check if running in production or testing
            if settings.DEBUG:
                update_weather(lat, lng)
            else:
                update_weather.delay(lat, lng)

            return redirect("weather")
        
    return render(
        request, 'weather/weather_view.html', {
            'current': current_weather,
            'forecast': forecast,
            'form': form,
        }
    )