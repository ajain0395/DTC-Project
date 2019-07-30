from django import forms
from .models import Stops
class LocationsForm(forms.ModelForm):
    class Meta:
        model = Stops
        fields = ('stop_name',)