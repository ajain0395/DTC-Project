from django.shortcuts import render
from django.views.generic import DetailView,TemplateView
from .models import Stops
from .models import Buses
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.db.models.query import QuerySet

from django.core.serializers import serialize
from django.http import HttpRequest, HttpResponse
# from stops.forms import StopsForm
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
import json

# class static_members():
#     pass
class FilterBuses:
    time = 15
    livetime = 2
    top_entries = 1
    vehicle_id = -1
    filter_field = ""
    route_id = []
    # last_point = {}
    def __init__(self):
        self.time = 15
        self.livetime = 2
        self.top_entries = 1
        self.vehicle_id = -1
        self.filter_field = ""
        self.route_id = []
        # self.last_point = {}
    def print_filters(self):
        print ("Routes Selected " + str(self.route_id))
        print ("Live Time" + str(self.livetime))
        print ("Vehicles Selected " + str(self.vehicle_id))
        print ("Field Selected " + str(self.filter_field))
        print ("Time delta Selected " + str(self.time))
        print ("Top Selected " + str(self.top_entries))

# request.session[buskey]. = FilterBuses()
buskey = 'busfilter'
page_id = "Stops"

def requestlivetime(request):
    return request['livetime']
def requestroutes(request):
    return request['route_id']
def requestvehicleids(request):
    return request['vehicle_id']
def requesttopentries(request):
    return request['top_entries']
def requestfilterfield(request):
    return request['filter_field']
def requesttime(request):
    return request['time']

class StopsTemplateView(TemplateView):
    """
        Stops detail view.
    """
    template_name = 'stops-detail.html'
    # model = Stops

    # def get(self, request):
    #     form = StopsForm()
    #     return render(request,self.template_name, {'form': form})

class StopsDetailView(DetailView):
    """
        Stops detail view.
    """
    template_name = 'stops-detail.html'
    model = Stops

class BusesDetailView(DetailView):
    """
        Buses detail view.
    """
    template_name = 'stops-detail.html'
    model = Buses

# def add_bus_to_list(request,vehicle_id):
#     request.session[buskey]['filter_field'] = "vehicle_id"
#     if(vehicle_id not in request.session[buskey]['vehicle_id']):
#         request.session[buskey]['vehicle_id'].append(vehicle_id)
#     request.session[buskey]['route_id'] = []
#     return particular_buses_multiple(request)

# def getvehicles_id(request):
#     3 = Buses.objects.filter(timestamp__gte=(timezone.now()-timedelta(minutes=request.session[buskey]['time'])))\
#         .order_by('vehicle_id','timestamp').distinct('vehicle_id').values('vehicle_id')
        


def particular_bus_id(request,vehicle_id):
    obj = Buses.objects.filter(vehicle_id=vehicle_id).order_by('-timestamp')[:request.session[buskey]['top_entries']]
    # print (len(obj))
    # print (obj[0].speed)
    #print (vehicle_id+"hello here")
    stops_points = serialize('geojson',obj)
    return HttpResponse(stops_points,content_type='json')
    # template_name = 'buses_id_details.html'
    # context = {"object":obj}
    # return render(request,template_name,context)
    #pass



def AllStops(request):
    stops_points = serialize('geojson',Stops.objects.all())
    return HttpResponse(stops_points,content_type='json')


from stops.forms import RVForm
from django.template import loader
from django.template import RequestContext
# Create your views here.

class HomePageView(TemplateView):
    template_name = "stops-detail.html"

    def get(self, request, **kwargs):
        print("inside get stops")
        request.session[buskey] = FilterBuses().__dict__
        print (request.session[buskey])
        form = RVForm()
        form.__init__()
        return render(request, self.template_name, {"form": form})

    def post(self, request, **kwargs):
        print("inside post stops")
        form = RVForm(request.POST)
        if form.is_valid():
            vehicle = form.getcleanedvehicle()
            print (vehicle)

            request.session[buskey]['vehicle_id'] = vehicle
        else:
            form = RVForm()
            
        return render(request, self.template_name, {"form": form})
    def all_buses_data(request):        
        queryres = Buses.objects.filter(timestamp__gte=(timezone.now()-timedelta(minutes=FilterBuses.livetime))).order_by('vehicle_id','-timestamp').distinct('vehicle_id')
        # q_ls = list(queryres)
        # return json.dumps(q_ls)
        buses_points = serialize('geojson',queryres)
        return HttpResponse(buses_points,content_type='json')

    def bus_route_line_data(request):
        cookiedata = request.session[buskey]
        sessionvehicle_ids = requestvehicleids(cookiedata)
        # sessionroute_ids = requestroutes(cookiedata)
        sessionlivetime = requestlivetime(cookiedata)
        sessiontopentries = requesttopentries(cookiedata)
        filtered_buses = Buses.objects.filter(vehicle_id=sessionvehicle_ids,
        timestamp__gte=(timezone.now()-timedelta(minutes=sessionlivetime))).order_by('-timestamp').values('latitude','longitude','congestion')[:2]
        # print (filtered_buses[0])
        # print (filtered_buses[1])
        q_ls = list(filtered_buses)
        return HttpResponse(json.dumps(q_ls),content_type='json')

    def particular_buses_multiple(request):
        # print_filters()
        cookiedata = request.session[buskey]
        print (cookiedata)

        sessionvehicle_ids = requestvehicleids(cookiedata)
        # sessionroute_ids = requestroutes(cookiedata)
        sessionlivetime = requestlivetime(cookiedata)
        sessiontopentries = requesttopentries(cookiedata)

        # filtered_buses = Buses.objects.none()
        # if(sessionvehicle_ids != -1):
        filtered_buses = Buses.objects.filter(vehicle_id=sessionvehicle_ids,
        timestamp__gte=(timezone.now()-timedelta(minutes=sessionlivetime))).order_by('-timestamp')[:1]

        # elif(len(sessionroute_ids) > 0 ):
        #     for i in range(0,len(sessionroute_ids)):
        #         filtered_buses = filtered_buses.union(Buses.objects.filter(route_id=sessionroute_ids[i],
        #     timestamp__gte=(timezone.now()-timedelta(minutes=sessionlivetime))).order_by('vehicle_id','-timestamp').distinct('vehicle_id'))
        # else:
        #     filtered_buses = filtered_buses.union(Buses.objects.filter(timestamp__gte=(timezone.now()-timedelta(minutes=FilterBuses.livetime))).order_by('vehicle_id','-timestamp').distinct('vehicle_id'))

        buses_points = serialize('geojson',filtered_buses)
        return HttpResponse(buses_points,content_type='json')
