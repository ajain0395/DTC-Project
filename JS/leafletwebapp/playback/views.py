from django.shortcuts import render
from django.views.generic import DetailView,TemplateView
from stops.models import Buses
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.serializers import serialize
from django.http import HttpRequest, HttpResponse
from django.utils import timezone
from datetime import timedelta
from django.utils.dateparse import parse_datetime
from .forms import Timerouteform
from django.template import loader
from django.template import RequestContext

class BusFilter:
    time = 15
    speed = 1
    startDate = ""
    endDate= ""
    route_id = ""
    vehicle_ids = ""


filterObj = BusFilter()



##########################################################33
#  if(len(filterBusesobj.route_id) > 0 and filterBusesobj.route_id[0] != -1):
#         for i in range(0,len(filterBusesobj.route_id)):
#             filtered_buses = filtered_buses.union(Buses.objects.filter(route_id=filterBusesobj.route_id[i],
#         timestamp__gte=(timezone.now()-timedelta(minutes=filterBusesobj.time))).order_by('vehicle_id','-timestamp').distinct('vehicle_id'))
###############################################################

def particular_buses_multiple(request):
    filtered_routes = Buses.objects.none()
    # if(len(filterBusesobj.vehicle_id) > 0 and filterBusesobj.vehicle_id[0] != -1):
    #     for i in range(0,len(filterBusesobj.vehicle_id)):
    #         filtered_buses = filtered_buses.union(Buses.objects.filter(vehicle_id=filterBusesobj.vehicle_id[i],
    #     timestamp__gte=(timezone.now()-timedelta(minutes=filterBusesobj.time))).order_by('-timestamp')[:filterBusesobj.top_entries])

    if(filterObj.startDate < filterObj.endDate):
        if(len(filterObj.route_id) > 0 and filterObj.route_id[0] != -1):
            for i in range(0,len(filterObj.route_id)):
                filtered_routes = filtered_routes.union(Buses.objects.filter(route_id=filterObj.route_id[i],
            timestamp__gte=filterObj.startDate,timestamp__lte=(filterObj.startDate + timedelta(seconds=10*filterObj.speed))).order_by('-timestamp'))
        filterObj.startDate = filterObj.startDate + timedelta(seconds=10*filterObj.speed)
    # print("filterrrrrrrrrr "+str(filtered_routes))

    buses_points = serialize('geojson',filtered_routes)
    print (filterObj.startDate)
    # filterObj.startDate = ""
    # filterObj.endDate = ""
    # filterObj.route_id = ""
    return HttpResponse(buses_points,content_type='json')


def appendTimeZone(playTime):
    playTime = str(playTime)
    timeList = playTime.split('+')
    newTime = timeList[0]+'+05:30'
    newTime = parse_datetime(newTime)
    return newTime


class playBackView(DetailView):
    template_name = 'playback.html'
    model = Buses
    formsrender = {}
    def get(self, request, **kwargs):
        # print("inside get")
        self.formsrender={}
        timerouteform = Timerouteform()
        self.formsrender['timeroute'] = timerouteform
        return render(request, self.template_name, self.formsrender)
        #return render(request, self.template_name)

    def post(self, request, **kwargs):
        print("inside post")
        self.formsrender={}
        timerouteform = Timerouteform(request.POST)
        print (request.POST)
        if(timerouteform.is_valid()):
            clean_route_id = timerouteform.cleaned_data['route_id_f']
            startDateTime = timerouteform.cleaned_data['startDateTime']
            endDateTime = timerouteform.cleaned_data['endDateTime']
                
            cleanStartDateTime = appendTimeZone(startDateTime)
            cleanEndDateTime = appendTimeZone(endDateTime)
            filterObj.route_id = clean_route_id
            filterObj.startDate = cleanStartDateTime
            filterObj.endDate = cleanEndDateTime
            if(timerouteform.getvehiclestate()==False):
                timerouteform.showvehicles()
            else:
                filterObj.vehicle_ids = timerouteform.getcleanedvehicles()
                timerouteform.hidevehicles()
        self.formsrender['timeroute'] = timerouteform
        return render(request, self.template_name, self.formsrender)        


        # if(timerouteform.is_valid()):
        #     timeroutevehicleform = VehicleForm(request.POST)
        #     if(timeroutevehicleform.is_valid()):
        #         print ("Both Valid Forms on Submit")
        #         clean_vehicle_id = timeroutevehicleform.cleaned_data['vehicle_id_f']
        #         print(clean_vehicle_id)
        #         filterObj.vehicle_ids = clean_vehicle_id
        #         self.formsrender['timeroute'] = timerouteform

        #     elif(timeroutevehicleform.is_valid() == False):
        #         print ("timeroute Valid only on Submit populatime vehicle")    
        #         clean_route_id = timerouteform.cleaned_data['route_id_f']
        #         startDateTime = timerouteform.cleaned_data['startDateTime']
        #         endDateTime = timerouteform.cleaned_data['endDateTime']
                
        #         cleanStartDateTime = parse_datetime(appendTimeZone(str(startDateTime)))
        #         cleanEndDateTime = parse_datetime(appendTimeZone(str(endDateTime)))

        #         filterObj.route_id = clean_route_id
        #         filterObj.startDate = cleanStartDateTime
        #         filterObj.endDate = cleanEndDateTime


        #         timeroutevehicleform = VehicleForm({'route':filterObj.route_id,
        #         'startDate':filterObj.startDate,
        #         'endDate':filterObj.endDate})
        #         self.formsrender['timeroute'] = timerouteform
        #         self.formsrender['timeroutevehicle'] = timeroutevehicleform
        # else:
        #     print ("timeroute not Valid only on Submit")
        #     # timerouteform = Timerouteform()
        #     self.formsrender['timeroute'] = timerouteform
            
            
        
       # return render(request, self.template_name)


# class vehiclePlayBackView(s):
#     template_name = 'VehiclePlayBack.html'

#     def get(self, request, **kwargs):
#         # print("inside get")
#         print("inside behicle--------------   get")
#         #form = VehicleForm()
#         # form  = MyForm()
#         filterObj.vehicle_id = []
#         form_class = VehicleForm({'route':filterObj.route_id,
#         'startDate':filterObj.startDate,
#         'endDate':filterObj.endDate})
        
#         # form = self.form_class()
#         return render(request, self.template_name, {'VehicleForm': form_class})
#         #return render(request, self.template_name)

#     def post(self, request, **kwargs):
#         print("inside behicle--------------   post")
#         form = VehicleForm(request.POST)
#         #form = VehicleForm()
#         if form.is_valid():
#             clean_vehicle_id = form.cleaned_data['vehicle_id_f']
#             print("inside --------------   post if behivle id ",clean_vehicle_id)
#             filterObj.vehicle_id = clean_vehicle_id
#         else:
#             print("inside --------------   post else")
#             filterObj.vehicle_id = []
#             form = VehicleForm({'route':filterObj.route_id,
#                     'startDate':filterObj.startDate,
#                     'endDate':filterObj.endDate})
#             #form2 = VehicleForm(filterObj.route_id,filterObj.startDate,filterObj.endDate)
#         return render(request, self.template_name,{"Vehicleform": form})
#         #return HttpResponseRedirect("")