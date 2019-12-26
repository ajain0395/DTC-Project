from django.shortcuts import render
from django.views.generic import DetailView,TemplateView
from stops.models import Buses
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.serializers import serialize
from django.http import HttpRequest, HttpResponse
from django.utils import timezone
from datetime import datetime

from datetime import timedelta
from django.utils.dateparse import parse_datetime
from .forms import Timerouteform
from django.template import loader
from django.template import RequestContext
from django.contrib import messages
import json
from .forms import routes_all_d

class BusFilter:
    time = 15
    speed = 1
    startDate = datetime.now().__str__()
    endDate= datetime.now().__str__()
    route_id = 0
    vehicle_id = -1
    vehicle_state = False
    def __init__(self):
        self.time = 15
        self.speed = 1
        self.startDate = datetime.now().__str__()
        self.endDate= datetime.now().__str__()
        self.route_id = 0
        self.vehicle_id = -1
        self.vehicle_state = False

session_key = "playbackfilter"
page_id = "Playback"


##########################################################33
#  if(len(filterBusesobj.route_id) > 0 and filterBusesobj.route_id[0] != -1):
#         for i in range(0,len(filterBusesobj.route_id)):
#             filtered_buses = filtered_buses.union(Buses.objects.filter(route_id=filterBusesobj.route_id[i],
#         timestamp__gte=(timezone.now()-timedelta(minutes=filterBusesobj.time))).order_by('vehicle_id','-timestamp').distinct('vehicle_id'))
###############################################################





def appendTimeZone(playTime):
    return playTime.__str__()
# def appendTimeZone(playTime):
#     playTime = str(playTime)
#     timeList = playTime.split('+')
#     newTime = timeList[0]+'+05:30'
#     newTime = parse_datetime(newTime)
#     return newTime

def parse_date_for_search(playTime):
    playTime = str(playTime)
    timeList = playTime.split('+')
    newTime = timeList[0]+'+05:30'
    newTime = parse_datetime(newTime)
    return newTime

def playbackresponse(request):
    cookie_data = request.session[session_key]
    parsed_start = parse_date_for_search(cookie_data['startDate'])
    parsed_end = parse_date_for_search(cookie_data['endDate'])
    print ("parsed_Start: ",parsed_start,", parsed_End: ",parsed_end)
    queryres = Buses.objects.filter(route_id=cookie_data['route_id'],timestamp__gte=parsed_start,timestamp__lte=parsed_end).distinct('vehicle_id').values('vehicle_id')
    # print (queryres)
    q_ls = list(queryres)
    # print (q_ls)
    return json.dumps(q_ls)

def congestionvalue(level):
    if(level == 0):
        return "Low"
    elif(level == 1):
        return 'Medium'
    return 'High'

class playBackView(TemplateView):
    template_name = 'playback.html'
    model = Buses
    formsrender = {}
    def get(self, request, **kwargs):
        print("inside get Playback")
        request.session[session_key] = BusFilter().__dict__
        self.formsrender={}
        timerouteform = Timerouteform()
        self.formsrender['timeroute'] = timerouteform
        print("getting out of get Playback")
        return render(request, self.template_name, self.formsrender)
        #return render(request, self.template_name)

    def post(self, request, **kwargs):
        print("inside post")
        # self.formsrender={}
        # timerouteform = Timerouteform(request.POST)
        # print (request.POST)
        # if(timerouteform.is_valid() or 'vehicle_id_f' in timerouteform.errors):
                

        #     print ("vehicle State ",filterObj.vehicle_state)
        #     if(filterObj.vehicle_state==False):
        #         clean_route_id = timerouteform.cleaned_data['route_id_f']
        #         startDateTime = timerouteform.cleaned_data['startDateTime']
        #         endDateTime = timerouteform.cleaned_data['endDateTime']
                    
        #         cleanStartDateTime = appendTimeZone(startDateTime)
        #         cleanEndDateTime = appendTimeZone(endDateTime)
        #         filterObj.route_id = clean_route_id
        #         filterObj.startDate = cleanStartDateTime
        #         filterObj.endDate = cleanEndDateTime
                
        #         print ("Showing Vehicles")
        #         timerouteform.showvehicles()
        #         filterObj.vehicle_state = True
                
        #         # timerouteform = Timerouteform({'oldform':timerouteform})
        #     else:
        #         print ("Hiding Vehicles")
        #         filterObj.vehicle_state = False
        #         request.POST = request.POST.copy()
        #         filterObj.vehicle_ids = request.POST.pop('vehicle_id_f')
        #         print ("printing here ",filterObj.vehicle_ids)

                
                
        #         # request.POST = request.POST.update({'vehicle_id_f':[]})
        #         # print (filterObj.vehicle_ids)
        #         timerouteform.hidevehicles()
        #     print ("REQUEST ",request.POST)
        # else:
        #     print ("Not Valid Form")
        #     print (timerouteform.errors)
        # self.formsrender['timeroute'] = timerouteform
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


    def updatestart(request):
        # filterObj.startDate 
        # print (request)
        # cookie_data = request.session[session_key]
        temp_data = appendTimeZone(request.GET.get('start_time'))
        request.session[session_key]['startDate'] = temp_data
        print ("start_time updated ",temp_data)
        
        return HttpResponse(playbackresponse(request),content_type='json')

    def updateend(request):
        temp_data = appendTimeZone(request.GET.get('end_time'))
        request.session[session_key]['endDate'] = temp_data
        print ("end_time updated ",temp_data)

        return HttpResponse(playbackresponse(request),content_type='json')

    def updatevehicle(request):
        temp_data = appendTimeZone(request.GET.get('vehicle_id'))
        request.session[session_key]['vehicle_id'] = temp_data
        print ("vehicle_id updated ",temp_data)

        return HttpResponse(request)  

    def vehiclesonroute(request):
        temp_data = appendTimeZone(request.GET.get('route_id'))
        request.session[session_key]['route_id'] = temp_data

        print ("route_id_updated ",temp_data)    
        # json_subcat = serialize("json", queryres)
        # print (json_subcat)
        return HttpResponse(playbackresponse(request),content_type='json')
        # print ("got in ",route_id)
        # return HttpResponse()

    def particular_buses_multiple(request):
        filtered_routes = Buses.objects.none()
        # if(filterObj.startDate == None):
        #     messages.info(request, 'Invalid Start Date')
        #     return HttpResponse(json.dumps([]),content_type='json')
        # elif(filterObj.endDate == None):
        #     messages.info(request, 'Invalid End Date')
        #     return HttpResponse(json.dumps([]),content_type='json')
        # elif(filterObj.vehicle_ids == -1 or filterObj.vehicle_ids == None):
        #     messages.info(request, 'Invalid Vehicle Id')
        #     return HttpResponse(json.dumps([]),content_type='json')
        # elif(filterObj.route_id == None or filterObj.route_id == -1):
        #     messages.info(request, 'Invalid Route')
        #     return HttpResponse(json.dumps([]),content_type='json')
        # elif(filterObj.startDate > filterObj.endDate):
        #     messages.info(request, 'Start Date cannot be greater than End Date')
        #     return HttpResponse(json.dumps([]),content_type='json')
        

        # if(len(filterBusesobj.vehicle_id) > 0 and filterBusesobj.vehicle_id[0] != -1):
        #     for i in range(0,len(filterBusesobj.vehicle_id)):
        #         filtered_buses = filtered_buses.union(Buses.objects.filter(vehicle_id=filterBusesobj.vehicle_id[i],
        #     timestamp__gte=(timezone.now()-timedelta(minutes=filterBusesobj.time))).order_by('-timestamp')[:filterBusesobj.top_entries])
        cookie_data = request.session[session_key]
        print ("---------------\n",cookie_data,"\n-----------------","\n")
        if(cookie_data['vehicle_id'] == -1):
            return HttpResponse()
        #route_id=cookie_data['route_id'],
        filtered_routes = Buses.objects.filter(vehicle_id=cookie_data['vehicle_id'],
        timestamp__gte=cookie_data['startDate'],timestamp__lte=cookie_data['endDate']).order_by('timestamp').values('latitude','longitude','route_id','congestion','timestamp')
        q_ls = []
        for i in filtered_routes:
            tmp = {}
            tmp['lng'] = i['longitude']
            tmp['lat'] = i['latitude']
            tmp['time'] = datetime.timestamp(i['timestamp'])
            tmp['info'] = [{'key':'Vehicle Id: ','value':cookie_data['vehicle_id']},
            {'key':'Route Id: ','value':routes_all_d[i['route_id']] +' ' + str(i['route_id'])},
            {'key':'Congestion: ','value':congestionvalue(i['congestion'])},
            {'key':'Time: ','value':str(i['timestamp'])}]
            # tmp['time'] = datetime.timestamp(i[j])
            
            q_ls.append(tmp)
        # while(True):
        #     if(filterObj.startDate < filterObj.endDate):
        #         if(len(filterObj.route_id) > 0 and len(filterObj.vehicle_ids) > 0):
        #             for i in range(0,len(filterObj.vehicle_ids)):
        #                 filtered_routes = filtered_routes.union(Buses.objects.filter(route_id=filterObj.route_id[i],vehicle_id = filterObj.vehicle_ids[i],
        #             timestamp__gte=filterObj.startDate,timestamp__lte=(filterObj.startDate + timedelta(seconds=10*filterObj.speed))).order_by('-timestamp'))
        #         if(filtered_routes.count() > 0):
        #             break
        #         filterObj.startDate = filterObj.startDate + timedelta(seconds=10*filterObj.speed)
        #     else:
        #         break
        # if(str != filterObj.startDate):
        #     filterObj.startDate = filterObj.startDate + timedelta(seconds=10*filterObj.speed)
        # print("filterrrrrrrrrr "+str(filtered_routes))
        # print ("LENGTH ",(filtered_routes))
        # buses_points = serialize('json',list(filtered_routes))
        # return json.dumps(q_ls)
        print ("returning playback data")
        return HttpResponse(json.dumps(q_ls),content_type='json')