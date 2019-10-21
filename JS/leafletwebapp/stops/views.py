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

# class static_members():
#     pass
class FilterBuses:
    time = 15
    top_entries = 1
    vehicle_id = []
    filter_field = ""
    route_id = []
    def __init__(self):
        self.time = 15
        self.top_entries = 1
        self.vehicle_id = []
        self.filter_field = ""
        self.route_id = []
    def print_filters(self):
        print ("Routes Selected " + str(self.route_id))
        print ("Vehicles Selected " + str(self.vehicle_id))
        print ("Field Selected " + str(self.filter_field))
        print ("Time delta Selected " + str(self.time))
        print ("Top Selected " + str(self.top_entries))

# request.session[buskey]. = FilterBuses()
buskey = 'busfilter'

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

def getvehicles_id(request):
    vehicles_id_list = Buses.objects.filter(timestamp__gte=(timezone.now()-timedelta(minutes=request.session[buskey]['time'])))\
        .order_by('vehicle_id','timestamp').distinct('vehicle_id').values('vehicle_id')
        


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

def AllBuses(request):
    buses_points = serialize('geojson',Buses.objects.all())
    return HttpResponse(buses_points,content_type='json')


from stops.forms import RVForm
from django.template import loader
from django.template import RequestContext
# Create your views here.

class HomePageView(TemplateView):
    template_name = "stops-detail.html"

    def get(self, request, **kwargs):
        print("inside get")
        request.session[buskey] = FilterBuses().__dict__
        print (request.session[buskey])
        form = RVForm()
        form.__init__()
        return render(request, self.template_name, {"form": form})

    def post(self, request, **kwargs):
        print("inside post")
        form = RVForm(request.POST)
        if form.is_valid():
            # vehicle_ids = form.cleaned_data['vehicle_id']
            # clean_vehicle_id =  form.cleaned_data['vehicle_id_f']
            # clean_route_id = form.cleaned_data['route_id_f']

            # if(len(clean_route_id) == 1 and )

            # request.session[buskey]['filter_field']="vehicle_id"
            # clean_vehicle_id = asd
            # print (clean_vehicle_id)
            # print (asd)
            # for i in asd.values():
            #     print (i['vehicle_id'])
            # for i in asd:
            #     print (i.vehicle_id)
            request.session[buskey]['vehicle_id'] = form.getcleanedvehicle()
            request.session[buskey]['route_id'] = form.getcleanedroutes()
            print ("hello " + str(request.POST))
            if "filterbus" in request.POST:
                print ("filterbus inside")
                # request.session.pop('filterbus')
                pass
            else:
                form = RVForm()
                print ("filterbus inside")
            # form.
        else:
            form = RVForm()
            
        return render(request, self.template_name, {"form": form})
    def particular_buses_multiple(request):
        # print_filters()
        print (request.session[buskey])
        filtered_buses = Buses.objects.none()
        if(len(request.session[buskey]['vehicle_id']) > 0 and request.session[buskey]['vehicle_id'][0] != -1):
            for i in range(0,len(request.session[buskey]['vehicle_id'])):
                filtered_buses = filtered_buses.union(Buses.objects.filter(vehicle_id=request.session[buskey]['vehicle_id'][i],
            timestamp__gte=(timezone.now()-timedelta(minutes=request.session[buskey]['time']))).order_by('-timestamp')[:request.session[buskey]['top_entries']])

        if(len(request.session[buskey]['route_id']) > 0 and request.session[buskey]['route_id'][0] != -1):
            for i in range(0,len(request.session[buskey]['route_id'])):
                filtered_buses = filtered_buses.union(Buses.objects.filter(route_id=request.session[buskey]['route_id'][i],
            timestamp__gte=(timezone.now()-timedelta(minutes=request.session[buskey]['time']))).order_by('vehicle_id','-timestamp').distinct('vehicle_id'))

        buses_points = serialize('geojson',filtered_buses)
        return HttpResponse(buses_points,content_type='json')
