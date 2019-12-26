from django import forms
# from easy_select2.widgets import Select2Multiple
from django_select2.forms import Select2MultipleWidget,Select2Widget
from stops.models import Buses
from django.utils import timezone
from datetime import timedelta
from django.forms import DateTimeField
from bootstrap_datepicker_plus import DateTimePickerInput  
from django.utils.dateparse import parse_datetime
import pandas as pd
import json


import numpy as np

import os 
# dir_path = os.path.dirname(os.path.realpath(__file__))
# print ("cur path ",dir_path)
routes_all = pd.read_csv('static/buses_static_data/routes.txt')
routes_all_d = {}
for i in range(len(routes_all)):
    routes_all_d[int(routes_all['route_id'][i])] = routes_all['route_long_name'][i]

# routes_all = routes_all.drop(columns=['route_short_name','route_type'])
# routes_all = np.array(routes_all)
def appendTimeZone(playTime):
    playTime = str(playTime)
    timeList = playTime.split('+')
    newTime = timeList[0]+'+05:30'
    newTime = parse_datetime(newTime)
    return newTime

def getvehicles(routeId, startTime,endTime):
    queryset_vehicle = Buses.objects.filter(route_id=routeId,timestamp__gte=startTime,timestamp__lte=endTime)\
    .order_by('vehicle_id','timestamp').distinct('vehicle_id').values('vehicle_id')
    vehicles = []
    # vehicles.append((-1,'---------'))
    for i in queryset_vehicle:
        vehicles.append((i['vehicle_id'],i['vehicle_id']))
    print ("vehicle list obtained -----",vehicles)
    return vehicles

def getroutes():
    # queryset_route = Buses.objects.order_by('route_id','timestamp').distinct('route_id').values('route_id')
    routes = []
    # routes.append((-1,'---------'))

    for i in routes_all_d.keys():
        routes.append((i,routes_all_d[i] + " - " + str(i)))
    return routes

class Timerouteform(forms.Form):
    def __init__(self, *args,**kwargs):
        super(Timerouteform, self).__init__(*args, **kwargs)
        self.fields['startDateTime'] = DateTimeField(label="Start Time",widget=DateTimePickerInput(format = "%Y-%m-%d %H:%M:%S",attrs={'placeholder': 'YYYY-MM-DD HH:MM:SS','id':'starttime'}),required=True,initial=timezone.now())
        self.fields['endDateTime'] = DateTimeField(label="End Time",widget=DateTimePickerInput(format = "%Y-%m-%d %H:%M:%S",attrs={'placeholder': 'YYYY-MM-DD HH:MM:SS','id':'endtime'}),required=True,initial=timezone.now())
        self.fields['route_id_f'] = forms.ChoiceField(label = "Route Id",choices=getroutes(),widget=Select2Widget(attrs={'id':'route_id_field','style':'width:96%'}),required=True)
        self.fields['vehicle_id_f'] = forms.ChoiceField(label = "Vehicle Id",widget=Select2Widget(attrs={'id':'vehicle_id_field','style':'width:96%'}),required=True)



    def getcleanedroutes(self):
        return self.cleaned_data.get("route_id_f")

    def getcleanedvehicles(self):
        return self.cleaned_data.get("vehicle_id_f")

    def getcleanedstarttime(self):
        return self.cleaned_data.get('startDateTime')

    def getcleanedendtime(self):
        return self.cleaned_data.get('endDateTime')

    def showvehicles(self,*args, **kwargs):
        choices = getvehicles(routeId= self.getcleanedroutes(),
        startTime=appendTimeZone(self.getcleanedstarttime()),
        endTime=appendTimeZone(self.getcleanedendtime()))
        
        # self.vehicle_state = True
        # print (choices[0])
        self.fields['vehicle_id_f'] = forms.ChoiceField(label = "Vehicle Ids",
                required=False,widget=Select2Widget,choices=choices)
        self.fields['route_id_f'].disabled=True
        self.fields['startDateTime'].disabled=True
        self.fields['endDateTime'].disabled=True
        # self.fields['vehicle_id_f'].widget = Select2Widget()
        # self.fields['vehicle_id_f'].initial = choices[0][0]
        # self.fields['vehicle_id_f'].required = True
        # super(Timerouteform, self).__init__(*args, **kwargs)
        
    def hidevehicles(self):
        self.fields.pop('vehicle_id_f')
        # choices = getvehicles(routeId= self.getcleanedroutes(),
        # startTime=appendTimeZone(self.getcleanedstarttime()),
        # endTime=appendTimeZone(self.getcleanedendtime()))
        # self.fields['vehicle_id_f'].widget = forms.HiddenInput()
        self.fields['route_id_f'].disabled= False
        self.fields['startDateTime'].disabled= False
        self.fields['endDateTime'].disabled= False
        # widget=Select2Widget