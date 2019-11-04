from django import forms
# from easy_select2.widgets import Select2Multiple
from django_select2.forms import Select2MultipleWidget,Select2Widget
from stops.models import Buses
from django.utils import timezone
from datetime import timedelta
from django.forms import DateTimeField
from django.utils.dateparse import parse_datetime

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
    queryset_route = Buses.objects.order_by('route_id','timestamp').distinct('route_id').values('route_id')
    routes = []
    # routes.append((-1,'---------'))
    for i in queryset_route:
        routes.append((i['route_id'],i['route_id']))
    return routes

class Timerouteform(forms.Form):
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
    route_id_f = forms.ChoiceField(label = "Route Ids",choices=getroutes(),widget=Select2Widget)
    vehicle_id_f = forms.ChoiceField(label = "Vehicle Ids",widget= forms.HiddenInput,required=False)
    vehicle_state = False
    # def __init__(self,timeroute, *args,**kwargs):
    #     print ("Inside new constructor")
    #     super(Timerouteform, timeroute).__init__(*args, **kwargs)
    #     # self.vehicle_state = False
    #     choices = getvehicles(routeId= timeroute.getcleanedroutes(),
    #     startTime=appendTimeZone(timeroute.getcleanedstarttime()),
    #     endTime=appendTimeZone(timeroute.getcleanedendtime()))
        
    #     self.vehicle_state = True
    #     # print (choices[0])
        
    #     self.fields['vehicle_id_f'] = forms.ChoiceField(label = "Vehicle Ids",
    #     required=True,widget=Select2Widget,choices=choices)

    def __init__(self, *args,**kwargs):
        super(Timerouteform, self).__init__(*args, **kwargs)

        # if(len(args) > 0):
        #     if('oldform' in args[0]):
        #         oldform = args[0]['oldform']

        #         print ("Inside new constructor")
        #         # super(Timerouteform, oldform).__init__(*args, **kwargs)
        #         # self.vehicle_state = False
        #         choices = getvehicles(routeId= oldform.getcleanedroutes(),
        #         startTime=appendTimeZone(oldform.getcleanedstarttime()),
        #         endTime=appendTimeZone(oldform.getcleanedendtime()))
        #         self.vehicle_state = True
        #         self.fields['route_id_f'].widget = forms.HiddenInput()
        #         self.fields['startDateTime'].widget = forms.HiddenInput()
        #         self.fields['endDateTime'].widget = forms.HiddenInput()
        #         self.fields['route_id_f'].required = False
        #         self.fields['startDateTime'].required = False
        #         self.fields['endDateTime'].required = False
        #         self.fields['vehicle_id_f'] = forms.ChoiceField(label = "Vehicle Ids",
        #         required=True,widget=Select2Widget,choices=choices)



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
        # self.fields['vehicle_id_f'].widget = Select2Widget()
        # self.fields['vehicle_id_f'].initial = choices[0][0]
        # self.fields['vehicle_id_f'].required = True
        # super(Timerouteform, self).__init__(*args, **kwargs)
        
    def hidevehicles(self):
        # choices = getvehicles(routeId= self.getcleanedroutes(),
        # startTime=appendTimeZone(self.getcleanedstarttime()),
        # endTime=appendTimeZone(self.getcleanedendtime()))
        self.fields['vehicle_id_f'].widget = forms.HiddenInput()
        # widget=Select2Widget

# class VehicleForm(forms.Form):
#     vehicle_id_f = forms.MultipleChoiceField(label = "Vehicle Ids",
#     widget=Select2MultipleWidget,
#     # required=False
#     )
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
#             # self.fields['vehicle_id_f'].initial = -1
#         # self.vehicle_id_f = forms.MultipleChoiceField(label = "Vehicle Ids",choices=getvehicles(route_id,startTime,endTime),initial=-1)
#         #print(self.cleaned_data.get('vehicle_id_f'))
#         #print(self.vehicle_id_f)
#     def getcleanedvehicle(self):
#         return self.cleaned_data.get('vehicle_id_f')