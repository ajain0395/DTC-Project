
from django import forms
from easy_select2.widgets import Select2Multiple
from .models import Buses
from django.utils import timezone
from datetime import timedelta
from .views import FilterBuses
# from django_select2.forms import (
#     HeavySelect2MultipleWidget, HeavySelect2Widget, ModelSelect2MultipleWidget,
#     ModelSelect2TagWidget, ModelSelect2Widget, Select2MultipleWidget,
#     Select2Widget
# )

def getvehicles():
    queryset_vehicle = Buses.objects.filter(timestamp__gte=(timezone.now()-timedelta(minutes=FilterBuses.time)))\
        .order_by('vehicle_id','timestamp').distinct('vehicle_id').values('vehicle_id')
    vehicles = []
    vehicles.append((-1,'---------'))
    for i in queryset_vehicle:
        vehicles.append((i['vehicle_id'],i['vehicle_id']))
    return vehicles

def getroutes():
    queryset_route = Buses.objects.filter(timestamp__gte=(timezone.now()-timedelta(minutes=FilterBuses.time)))\
        .order_by('route_id','timestamp').distinct('route_id').values('route_id')
    # print (str(queryset.query))
    
    routes = []
    routes.append((-1,'---------'))
    # queryset = queryset.order_by('-timestamp')
    # print ('NewForm')
    
    for i in queryset_route:
        routes.append((i['route_id'],i['route_id']))
    return routes

class RVForm(forms.Form):

    vehicle_id_f = forms.MultipleChoiceField(label = "Vehicle Ids",choices=getvehicles(),
    #  widget=Select2Multiple(select2attrs={'width': 'auto'}),
     initial=-1)
    route_id_f = forms.MultipleChoiceField(label = "Route Ids",choices=getroutes(),
    #  widget=Select2Multiple(select2attrs={'width': 'auto'}),
     initial=-1)
