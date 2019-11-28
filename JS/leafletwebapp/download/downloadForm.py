from django import forms
from django.forms import DateTimeField
from django.utils.dateparse import parse_datetime

class DownloadForm(forms.Form):
    #Date = DateTimeField(widget=forms.SelectDateWidget())
    Date = DateTimeField(widget=forms.TextInput(attrs={'class':'datetime-input'}))
    vehicle_id = forms.CharField(label="Vehicle Id",widget=forms.TextInput(attrs={'placeholder': 'enter vehicle id'}),required=False)
    route_id = forms.CharField(label="Route Id",widget=forms.TextInput(attrs={'placeholder': 'enter route id'}),required=False)
    #check_me_out = forms.BooleanField(label="Check to proceed")

    def getcleanedvehicle(self):
        return self.cleaned_data.get("vehicle_id")
    def getcleanedroutes(self):
        return self.cleaned_data.get("route_id")
   