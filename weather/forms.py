# weather/forms.py
from django import forms


class LocationForm(forms.Form):
    city = forms.CharField(max_length=100, required=True)
    state = forms.CharField(max_length=100, required=True)
    country = forms.CharField(max_length=100, required=True)
