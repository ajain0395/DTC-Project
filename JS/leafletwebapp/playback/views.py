from django.shortcuts import render
from django.views.generic import DetailView,TemplateView
# from .models import Buses
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.serializers import serialize
from django.http import HttpRequest, HttpResponse
from django.utils import timezone
from datetime import timedelta
# from stops.forms import MyForm
from django.template import loader
from django.template import RequestContext

class FilterBuses:
    time = 15
    speed = ""
    date = ""
    route_id = ""


filterBusesobj = FilterBuses()


# def particular_route_playback(request):
#     filtered_buses = Buses.objects.filter(route_id='174')
#     buses_points = serialize('geojson',filtered_buses)
#     return HttpResponse(buses_points,content_type='json')

class playBackView(DetailView):
    template_name = 'playback.html'
    # model = Buses
    
    def get(self, request, **kwargs):
        print("inside get")
        # form = MyForm()
        # return render(request, self.template_name, {"form": form})
        return render(request, self.template_name)

    def post(self, request, **kwargs):
        print("inside get")
        # form = MyForm(request.POST)
        # if form.is_valid():
        #     # vehicle_ids = form.cleaned_data['vehicle_id']
        #     asd =  form.cleaned_data['name']
        #     filterBusesobj.filter_field="vehicle_id"
        #     clean_vehicle_id = asd
        #     print (clean_vehicle_id)
        #     print (asd)
        #     # for i in asd.values():
        #     #     print (i['vehicle_id'])
        #     # for i in asd:
        #     #     print (i.vehicle_id)
        #     filterBusesobj.vehicle_id = clean_vehicle_id
            
        # return render(request, self.template_name, {"form": form})
        return render(request, self.template_name)