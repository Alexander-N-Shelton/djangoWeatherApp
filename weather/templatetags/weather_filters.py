# weather/templatetags/weather_filters.py
from django import template

register = template.Library()

@register.filter
def weather_icon(code, is_forecast=True):
    """Returns the correct weather icon filename."""
    match code:
        case 0:
            base_icon = "clear"
        case 1:
            base_icon = "cloudy-1"
        case 2:
            base_icon = "cloudy-2"
        case 3:
            base_icon = "cloudy-3"
        case 45 | 48:
            base_icon = "fog"
        case 51 | 61 | 80:
            base_icon = "rainy-1"
        case 53 | 63 | 81:
            base_icon = "rainy-2"
        case 55 | 65 | 82:
            base_icon = "rainy-3"
        case 56 | 57 | 66 | 67:
            base_icon = "rain-and-sleet-mix"
        case 71 | 77:
            base_icon = "snowy-1"
        case 73 | 85:
            base_icon = "snowy-2"
        case 75 | 86:
            base_icon = "snowy-3"
        case 95 | 96:
            base_icon = "scattered-thunderstorms"
        case 99:
            base_icon = "severe-thunderstorms"
        case _:
            base_icon = "unknown"

    # If it's a forecast, always return the day version
    return f"weather-icons/{base_icon}-day.svg"
