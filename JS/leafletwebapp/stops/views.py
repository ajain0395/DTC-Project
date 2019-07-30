from django.shortcuts import render
from django.views.generic import DetailView,TemplateView
from .models import Stops
from django.core.serializers import serialize
from django.http import HttpRequest, HttpResponse

class StopsTemplateView(TemplateView):
    """
        Stops detail view.
    """
    template_name = 'stops-detail.html'
    # model = Stops
class StopsDetailView(DetailView):
    """
        Stops detail view.
    """
    template_name = 'stops-detail.html'
    model = Stops
# Create your views here.

# from .forms import LocationsForm

def AllStops(request):
    stops_points = serialize('geojson',Stops.objects.all())
    return HttpResponse(stops_points,content_type='json')

# def LocationsView(request):
#     form = LocationsForm
#     return render(request, 'stops-detail.html', {'form': form})