
from django import forms
from easy_select2.widgets import Select2Multiple
from .models import Buses
from django.utils import timezone
from datetime import timedelta
from .views import filterBusesobj
class MyForm(forms.Form):
#  name = forms.CharField(label='Enter your name', max_length=100)
#  email = forms.EmailField(label='Enter your email', max_length=100)
    # vehicle_id = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "5", }))
    queryset = Buses.objects.distinct('vehicle_id').filter(timestamp__gte=(timezone.now()-timedelta(minutes=filterBusesobj.time))).values('vehicle_id')
    # print (str(queryset.query))
    vehicles = []
    vehicles.append(('-----','-----'))
    # queryset = queryset.order_by('-timestamp')
    for i in queryset:
        vehicles.append((i['vehicle_id'],i['vehicle_id']))
    # print (queryset.values())
    # print (vehicles)
    # vehicles = vehicles.reverse()
    name = forms.MultipleChoiceField(label = "Vehicle Ids",choices=vehicles,widget=Select2Multiple(
            select2attrs={'width': '100%'}
        ))
