
from django import forms
from django_select2.forms import Select2Widget
from .models import Buses
from django.utils import timezone
from datetime import timedelta
from .views import FilterBuses
from playback.forms import routes_all_d
import pandas as pd
# from django_select2.forms import (
#     HeavySelect2MultipleWidget, HeavySelect2Widget, ModelSelect2MultipleWidget,
#     ModelSelect2TagWidget, ModelSelect2Widget, Select2MultipleWidget,
#     Select2Widget
# )

import os 
dir_path = os.path.dirname(os.path.realpath(__file__))
print ("cur path ",dir_path)
routes_all = pd.read_csv('static/buses_static_data/routes.txt')
routes_all_d = {}
for i in range(len(routes_all)):
    routes_all_d[int(routes_all['route_id'][i])] = routes_all['route_long_name'][i]

def getvehicles():
    queryset_vehicle = Buses.objects.filter(timestamp__gte=(timezone.now()-timedelta(minutes=FilterBuses.livetime)))\
        .order_by('vehicle_id','timestamp').distinct('vehicle_id').values('vehicle_id','route_id')
    vehicles = []
    vehicles_dict = {}
    vehicles.append((-1,'------------'))
    for i in queryset_vehicle:
        if(i['route_id'] not in vehicles_dict):
            vehicles_dict[i['route_id']] = []
        vehicles_dict[i['route_id']].append((i['vehicle_id'],i['vehicle_id']))
    for i in vehicles_dict.keys():
        vehicles.append((routes_all_d[i] + ' - '+ str(i),vehicles_dict[i]))
    return vehicles

def getroutes():
    queryset_route = Buses.objects.filter(timestamp__gte=(timezone.now()-timedelta(minutes=FilterBuses.livetime)))\
        .order_by('route_id','timestamp').distinct('route_id').values('route_id')
    # print (str(queryset.query))
    
    routes = []
    # routes.append((-1,'---------'))
    # queryset = queryset.order_by('-timestamp')
    # print ('NewForm')
    
    for i in queryset_route:
        routes.append((i['route_id'],routes_all_d[i['route_id']] + " - "+str(i['route_id'])))
    return routes

class RVForm(forms.Form):
    vehicle_id_f = forms.ChoiceField(label = "Vehicle Ids",choices=getvehicles(),
    widget=Select2Widget(attrs={'id':'vehicle_id_field_live'}),required=False,
     initial=-1)
    # widget=forms.SelectMultiple(attrs={'id':"boot-multiselect-demo" ,'multiple':"multiple"}),initial=-1)
    # route_id_f = forms.MultipleChoiceField(label = "Route Ids",choices=getroutes(),
    #  widget=Select2MultipleWidget(attrs={'id':'route_id_field_live'}),required=False,
    #  initial=-1
    #  )

    def __init__(self, *args,**kwargs):
        super(RVForm, self).__init__(*args, **kwargs)
        self.fields['vehicle_id_f'].choices = getvehicles()
        # self.fields['route_id_f'].choices = getroutes()
        # self.vehicle_id_f = forms.MultipleChoiceField(label = "Vehicle Ids",choices=getvehicles(),
        # initial=-1)
        # self.route_id_f = forms.MultipleChoiceField(label = "Route Ids",choices=getroutes(),
        # initial=-1)
    def getcleanedvehicle(self):
        return self.cleaned_data.get("vehicle_id_f")
    def getcleanedroutes(self):
        return self.cleaned_data.get("route_id_f")
    def getcleanedboth(self):
        X = self.getcleanedvehicle()
        Y = self.getcleanedroutes()
        if(len(X) == 0 and len(Y) == 0):
            self._errors['vehicle_id_f'] = self.error_class(['Select 1 Vehicle or Route First'])
            return [],[]
            # self._errors['vehicle_id_f'] = self.error_class(['Minimum 5 characters required'])
        return X,Y
        