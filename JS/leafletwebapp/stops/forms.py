
from django import forms
from easy_select2.widgets import Select2Multiple
from .models import Buses
from django.utils import timezone
from datetime import timedelta
from .views import filterBusesobj
# from django_select2.forms import (
#     HeavySelect2MultipleWidget, HeavySelect2Widget, ModelSelect2MultipleWidget,
#     ModelSelect2TagWidget, ModelSelect2Widget, Select2MultipleWidget,
#     Select2Widget
# )

class RVForm(forms.Form):
#  name = forms.CharField(label='Enter your name', max_length=100)
#  email = forms.EmailField(label='Enter your email', max_length=100)
    # vehicle_id = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "5", }))
    queryset_vehicle = Buses.objects.filter(timestamp__gte=(timezone.now()-timedelta(minutes=filterBusesobj.time)))\
        .order_by('vehicle_id','timestamp').distinct('vehicle_id').values('vehicle_id')
    queryset_route = Buses.objects.filter(timestamp__gte=(timezone.now()-timedelta(minutes=filterBusesobj.time)))\
        .order_by('route_id','timestamp').distinct('route_id').values('route_id')
    # print (str(queryset.query))
    vehicles = []
    vehicles.append((-1,'---------'))
    routes = []
    routes.append((-1,'---------'))
    # queryset = queryset.order_by('-timestamp')
    # print ('NewForm')
    for i in queryset_vehicle:
        vehicles.append((i['vehicle_id'],i['vehicle_id']))
    for i in queryset_route:
        routes.append((i['route_id'],i['route_id']))
    # print (queryset.values())
    # print (vehicles)
    # vehicles = vehicles.reverse()
    vehicle_id_f = forms.MultipleChoiceField(label = "Vehicle Ids",choices=vehicles,
    #  widget=Select2Multiple(select2attrs={'width': 'auto'}),
     initial=vehicles[0])
    route_id_f = forms.MultipleChoiceField(label = "Route Ids",choices=routes,
    #  widget=Select2Multiple(select2attrs={'width': 'auto'}),
     initial=routes[0])
