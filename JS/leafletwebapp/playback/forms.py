from django import forms
from easy_select2.widgets import Select2Multiple
from stops.models import Buses
from django.utils import timezone
from datetime import timedelta
from django.forms import DateTimeField


#from .views import filterObj
from django_select2.forms import (
    HeavySelect2MultipleWidget, HeavySelect2Widget, ModelSelect2MultipleWidget,
    ModelSelect2TagWidget, ModelSelect2Widget, Select2MultipleWidget,
    Select2Widget
)

class MyForm(forms.Form):
    queryset_route = Buses.objects.filter(timestamp__gte=(timezone.now()-timedelta(minutes=15))).order_by('route_id','timestamp').distinct('route_id').values('route_id')
    routes = []
    routes.append((-1,'---------'))

    #startDate = DateTimeField(widget=forms.SelectDateWidget())
    #startTime = DateTimeWidget(usel10n=True)
    startDateTime= DateTimeField(input_formats=["%Y-%m-%d %H:%M:%S"],widget=forms.TextInput(attrs={'placeholder': '%Y-%m-%d %H:%M:%S'}))
    endDateTime= DateTimeField(input_formats=["%Y-%m-%d %H:%M:%S"],widget=forms.TextInput(attrs={'placeholder': '%Y-%m-%d %H:%M:%S'}))
    #print(startDateTime)
    for i in queryset_route:
        routes.append((i['route_id'],i['route_id']))
    
    route_id_f = forms.MultipleChoiceField(label = "Route Ids",choices=routes,widget=Select2Multiple,initial=routes[0])
    #print("heloooooooooooooooooooooooooo"+str(route_id_f))