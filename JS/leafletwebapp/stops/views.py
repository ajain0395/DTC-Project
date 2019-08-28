from django.shortcuts import render
from django.views.generic import DetailView,TemplateView
from .models import Stops
from .models import Buses
from django.shortcuts import render
from django.core.serializers import serialize
from django.http import HttpRequest, HttpResponse
from stops.forms import StopsForm
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

def print_filters():
    print ("Routes Selected " + str(FilterBuses.route_id))
    print ("Vehicles Selected " + str(FilterBuses.vehicle_id))
    print ("Field Selected " + str(FilterBuses.filter_field))
    print ("Time delta Selected " + str(FilterBuses.time))
    print ("Top Selected " + str(FilterBuses.top_entries))

def particular_buses_multiple(request):
    print_filters()
    if(len(FilterBuses.vehicle_id) > 0 and FilterBuses.filter_field == 'vehicle_id'):
        filtered_buses = Buses.objects.filter(vehicle_id=FilterBuses.vehicle_id[0],
        timestamp__gte=(timezone.now()-timedelta(minutes=FilterBuses.time))).order_by('-timestamp')[:FilterBuses.top_entries]
        for i in range(1,len(FilterBuses.vehicle_id)):
            filtered_buses = filtered_buses.union(Buses.objects.filter(vehicle_id=FilterBuses.vehicle_id[i],
        timestamp__gte=(timezone.now()-timedelta(minutes=FilterBuses.time))).order_by('-timestamp')[:FilterBuses.top_entries])

    elif(len(FilterBuses.route_id) > 0 and FilterBuses.filter_field == 'route_id'):
        filtered_buses = Buses.objects.filter(vehicle_id__in=FilterBuses.vehicle_id,
        timestamp__gte=(timezone.now()-timedelta(minutes=FilterBuses.time))).order_by('-timestamp')[:FilterBuses.top_entries]

    else:
        filtered_buses = Buses.objects.all().order_by('-timestamp')[:50]
    buses_points = serialize('geojson',filtered_buses)
    return HttpResponse(buses_points,content_type='json')

def add_bus_to_list(request,vehicle_id):
    FilterBuses.filter_field = "vehicle_id"
    if(vehicle_id not in FilterBuses.vehicle_id):
        FilterBuses.vehicle_id.append(vehicle_id)
    FilterBuses.route_id = []
    return particular_buses_multiple(request)


def particular_bus_id(request,vehicle_id):
    obj = Buses.objects.filter(vehicle_id=vehicle_id).order_by('-timestamp')[:FilterBuses.top_entries]
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

def getspecificbus(request,vehicle_id):
    queryset = serialize('geojson',Buses.objects.filter(vehicle_id=vehicle_id))
    return HttpResponse(buses_points,content_type='json')


# def LocationsView(request):
#     form = LocationsForm
#     return render(request, 'stops-detail.html', {'form': form})