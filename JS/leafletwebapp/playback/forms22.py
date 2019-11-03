from django import forms
from easy_select2.widgets import Select2Multiple
from stops.models import Buses
from django.utils import timezone
from datetime import timedelta
from django.forms import DateTimeField



#from .views import filterObj
# from django_select2.forms import (
#     HeavySelect2MultipleWidget, HeavySelect2Widget, ModelSelect2MultipleWidget,
#     ModelSelect2TagWidget, ModelSelect2Widget, Select2MultipleWidget,
#     Select2Widget
# )

def getvehicles(routeId, startTime,endTime):
    queryset_vehicle = Buses.objects.filter(route_id=routeId,timestamp__gte=startTime,timestamp__lte=endTime)\
    .order_by('vehicle_id','timestamp').distinct('vehicle_id').values('vehicle_id')
    vehicles = []
    vehicles.append((-1,'---------'))
    for i in queryset_vehicle:
        vehicles.append((i['vehicle_id'],i['vehicle_id']))
    print ("vehicle list obtained -----",vehicles)
    return vehicles

def getroutes():
    queryset_route = Buses.objects.order_by('route_id','timestamp').distinct('route_id').values('route_id')
    routes = []
    routes.append((-1,'---------'))
    for i in queryset_route:
        routes.append((i['route_id'],i['route_id']))
    return routes

class MyForm(forms.Form):
    # class Meta:
    #     fields = ('startDateTime', 'endDateTime', 'route_id_f', 'vehicle_id_f')
    # queryset_route = Buses.objects.order_by('route_id','timestamp').distinct('route_id').values('route_id')
    # routes = []
    # routes.append((-1,'---------'))

    # #startDate = DateTimeField(widget=forms.SelectDateWidget())
    # #startTime = DateTimeWidget(usel10n=True)
    # #timestamp = forms.DateField(widget=forms.DateInput(attrs={'class':'timepicker'}))
    # startDateTime= DateTimeField(input_formats=["%Y-%m-%d %H:%M:%S"],widget=forms.TextInput(attrs={'placeholder': 'YYYY-mm-dd HH:MM:SS'}))
    # endDateTime= DateTimeField(input_formats=["%Y-%m-%d %H:%M:%S"],widget=forms.TextInput(attrs={'placeholder': 'Y-mm-dd HH:MM:SS'}))
    # #print(startDateTime)
    # for i in queryset_route:
    #     routes.append((i['route_id'],i['route_id']))
    
    # route_id_f = forms.MultipleChoiceField(label = "Route Ids",choices=routes,widget=Select2Multiple,initial=routes[0])
    # #print("heloooooooooooooooooooooooooo"+str(route_id_f))

    startDateTime= DateTimeField(input_formats=["%Y-%m-%d %H:%M:%S"],widget=forms.TextInput(attrs={'placeholder': 'YYYY-mm-dd HH:MM:SS'}))
    endDateTime= DateTimeField(input_formats=["%Y-%m-%d %H:%M:%S"],widget=forms.TextInput(attrs={'placeholder': 'YYYY-mm-dd HH:MM:SS'}))
    route_id_f = forms.ChoiceField(label = "Route Ids",choices=getroutes(),initial=-1)

    # def __init__(self, *args,**kwargs):
    #     super(MyForm, self).__init__(*args, **kwargs)
    #     # self.vehicle_id_f = forms.MultipleChoiceField(label = "Vehicle Ids",choices=getvehicles(),
    #     # initial=-1)
    #     self.route_id_f = forms.MultipleChoiceField(label = "Route Ids",choices=getroutes(),
    #     initial=-1)
    # # def getcleanedvehicle(self):
    # #     return self.cleaned_data.get("vehicle_id_f")
    # def getcleanedroutes(self):
    #     return self.cleaned_data.get("route_id_f")


# class VehicleForm(forms.Form):
#     vehicle_id_f = forms.MultipleChoiceField(label = "Vehicle Ids",choices=[(-1,"---------")],initial=-1)
#     # vehicle_id_f=[] 
  

#     def __init__(self, *args, **kwargs):
#         super(VehicleForm,self).__init__(*args, **kwargs)
#         data = args[0]
#         print ("form  ------- args  ",args)
#         #print (args[0])
#         # # print (kwargs)
#         # print (kwargs['kwargs'])
#         # print (len(kwargs['kwargs']))
#         # print (type(kwargs['kwargs']))
#         # print (kwargs.values()[0])
#         if('route' in data):
#             self.fields['vehicle_id_f'].choices = getvehicles(data['route'],data['startDate'],
#             data['endDate'])
#             self.fields['vehicle_id_f'].initial = -1
#         # self.vehicle_id_f = forms.MultipleChoiceField(label = "Vehicle Ids",choices=getvehicles(route_id,startTime,endTime),initial=-1)
#         #print(self.cleaned_data.get('vehicle_id_f'))
#         #print(self.vehicle_id_f)
#     # def getcleanedvehicle(self):
#     #     return self.cleaned_data.get('vehicle_id_f')