from django.shortcuts import render
from django.views.generic import DetailView,TemplateView
from stops.models import Buses
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.serializers import serialize
from django.http import HttpRequest, HttpResponse
from django.utils import timezone
from datetime import timedelta
from .forms import MyForm
from django.template import loader
from django.template import RequestContext

class BusFilter:
    time = 15
    speed = ""
    startDate = ""
    endDate= ""
    route_id = ""


filterObj = BusFilter()

def particular_buses_multiple(request):
    filtered_buses = Buses.objects.none()
    # if(len(filterBusesobj.vehicle_id) > 0 and filterBusesobj.vehicle_id[0] != -1):
    #     for i in range(0,len(filterBusesobj.vehicle_id)):
    #         filtered_buses = filtered_buses.union(Buses.objects.filter(vehicle_id=filterBusesobj.vehicle_id[i],
    #     timestamp__gte=(timezone.now()-timedelta(minutes=filterBusesobj.time))).order_by('-timestamp')[:filterBusesobj.top_entries])

    if(len(filterObj.route_id) > 0 and filterObj.route_id[0] != -1):
        for i in range(0,len(filterObj.route_id)):
            filtered_buses = filtered_buses.union(Buses.objects.filter(route_id=filterObj.route_id[i],
        timestamp__gte=(timezone.now()-timedelta(minutes=filterObj.time))).order_by('vehicle_id','-timestamp').distinct('vehicle_id'))

    buses_points = serialize('geojson',filtered_buses)
    return HttpResponse(buses_points,content_type='json')

def appendTimeZone(playTime):
    timeList = playTime.split('+')
    newTime = timeList[0]+'+05:30'
    return newTime


class playBackView(DetailView):
    template_name = 'playback.html'
    model = Buses
    
    def get(self, request, **kwargs):
        # print("inside get")
        form = MyForm()
        return render(request, self.template_name, {"formp": form})
        #return render(request, self.template_name)

    def post(self, request, **kwargs):
        print("inside get")
        form = MyForm(request.POST)
        if form.is_valid():
            clean_route_id = form.cleaned_data['route_id_f']
            startDateTime = form.cleaned_data['startDateTime']
            endDateTime = form.cleaned_data['endDateTime']
            
            cleanStartDateTime = appendTimeZone(str(startDateTime))
            cleanEndDateTime = appendTimeZone(str(endDateTime))
            #print("new start and end time "+cleanStartDateTime+"\t"+cleanEndDateTime)
            filterObj.route_id = clean_route_id
            filterObj.startDate = cleanStartDateTime
            filterObj.endDate = cleanEndDateTime
            
        return render(request, self.template_name, {"formp": form})
       # return render(request, self.template_name)