from django import forms
from django.forms import DateTimeField
from django.utils.dateparse import parse_datetime
from bootstrap_datepicker_plus import DateTimePickerInput ,DatePickerInput 
from django_select2.forms import Select2MultipleWidget,Select2Widget
import pandas as pd
import numpy as np
import os 


dir_path = os.path.dirname(os.path.realpath(__file__))
#print ("cur path ",dir_path)
routes_all = pd.read_csv('static/buses_static_data/routes.txt')
routes_all_d = {}
for i in range(len(routes_all)):
    routes_all_d[int(routes_all['route_id'][i])] = routes_all['route_long_name'][i]


def getroutes():
    # queryset_route = Buses.objects.order_by('route_id','timestamp').distinct('route_id').values('route_id')
    routes = []
    # routes.append((-1,'---------'))
    #print(routes_all_d.keys())
    for i in routes_all_d.keys():
        routes.append((i,routes_all_d[i] + " - " + str(i)))
    return routes

class DownloadForm(forms.Form):
    #Date = DateTimeField(widget=forms.SelectDateWidget())
    startDate= DateTimeField(widget=DatePickerInput(format = "%Y-%m-%d",attrs={'placeholder': 'YYYY-MM-DD','id':'download_startDate','class':'datetime-input'}),required=True)
    #endDateTime= DateTimeField(widget=DateTimePickerInput(format = "%Y-%m-%d %H:%M:%S",attrs={'placeholder': 'YYYY-MM-DD','id':'download_endtime'}),required=True)
    #startDate = DateTimeField(widget=forms.TextInput(attrs={'class':'datetime-input'}))
    vehicle_id = forms.CharField(label="Vehicle Id",widget=forms.TextInput(attrs={'placeholder': '','id':'download_vehicle_id_field'}),required=False)
    route_id_f = forms.ChoiceField(label = "Route Ids",choices=getroutes(),widget=Select2Widget(attrs={'id':'download_route_id_field','style':'width:100%'}),required=False)
    #route_id = forms.CharField(label="Route Id",widget=forms.TextInput(attrs={'placeholder': 'enter route id'}),required=False)
    
    #check_me_out = forms.BooleanField(label="Check to proceed")

    def getcleanedvehicle(self):
        return self.cleaned_data.get("vehicle_id")
    def getcleanedroutes(self):
        return self.cleaned_data.get("route_id_f")
   