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
from .forms import MyForm
from django.template import loader
from django.template import RequestContext

class BusFilter:
    time = 15
    speed = 1
    startDate = ""
    endDate= ""
    route_id = ""


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
    # print("filterrrrrrrrrr "+str(filtered_routes))

    buses_points = serialize('geojson',filtered_routes)
    filterObj.startDate = filterObj.startDate + timedelta(seconds=10*filterObj.speed)
    print (filterObj.startDate)
    # filterObj.startDate = ""
    # filterObj.endDate = ""
    # filterObj.route_id = ""
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
            
            #print("beforeeeeeeeeeeee ty "+str(type(startDateTime)))
            cleanStartDateTime = parse_datetime(appendTimeZone(str(startDateTime)))
            cleanEndDateTime = parse_datetime(appendTimeZone(str(endDateTime)))
            #print("afterrrrrrrrrrrrrrrr ty "+str(type(cleanStartDateTime)))
            #print("new start and end time "+cleanStartDateTime+"\t"+cleanEndDateTime)
            
            filterObj.route_id = clean_route_id
            filterObj.startDate = cleanStartDateTime
            filterObj.endDate = cleanEndDateTime
            
        return render(request, self.template_name, {"formp": form})
       # return render(request, self.template_name)