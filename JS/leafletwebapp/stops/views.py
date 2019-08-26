from django.shortcuts import render
from django.views.generic import DetailView,TemplateView
from .models import Stops
from .models import Buses
from django.shortcuts import render
from django.core.serializers import serialize
from django.http import HttpRequest, HttpResponse
from stops.forms import StopsForm

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