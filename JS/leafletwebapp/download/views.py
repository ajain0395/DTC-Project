from django.shortcuts import render,redirect
from django.views.generic import DetailView,TemplateView
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.core.serializers import serialize
from django.http import HttpRequest, HttpResponse
from .downloadForm import DownloadForm
from django.contrib import messages
from datetime import timedelta
from stops.models import Buses
# Create your views here.


def getData(date,vehicle_id,route_id):
    filtered_routes = Buses.objects.none()

    if(len(vehicle_id) > 0 and len(route_id) ==0 ):
        filtered_routes = filtered_routes.union(Buses.objects.filter(vehicle_id=vehicle_id,
        timestamp__gte=date,timestamp__lte=(date + timedelta(days=1))).order_by('timestamp'))

    elif(len(route_id) > 0 and len(vehicle_id) ==0 ):
        filtered_routes = filtered_routes.union(Buses.objects.filter(route_id=route_id,
        timestamp__gte=date,timestamp__lte=(date + timedelta(days=1))).order_by('timestamp'))
    else:
        filtered_routes = filtered_routes.union(Buses.objects.filter(route_id=route_id,vehicle_id = vehicle_id,
        timestamp__gte=date,timestamp__lte=(date + timedelta(days=1))).order_by('timestamp'))
        
    
    #print ("LENGTH ",(filtered_routes))
    buses_points = serialize('geojson',filtered_routes)

    # return buses_points 
   
    return HttpResponse(buses_points,content_type='json')



class downloadView(DetailView):
    template_name = 'download.html'
    
    
    def get(self, request):
        downloadForm = DownloadForm()
        return render(request, self.template_name,{"downloadForm":downloadForm})
    
        
    def post(self, request):
        # current_user = request.user
        downloadForm = DownloadForm(request.POST)
        
        if downloadForm.is_valid():
            date = downloadForm.cleaned_data['Date']
            vehicle = downloadForm.getcleanedvehicle()
            route = downloadForm.getcleanedroutes()
            
            # if(vehicle is None and route is None): 
            if(len(vehicle)==0 and len(route)==0): 
                messages.info(request, 'Select Vehicle or Route First')
            else:

                json_data = getData(date,vehicle,route)
                return json_data
                #html = render_to_string()
                #return HttpResponse({'json_data':json_data}, 'demo.html',content_type="application/html")
                #return redirect(request, 'demo.html', {'json_data': json_data })
        

        return render(request, self.template_name, {'downloadForm': downloadForm})