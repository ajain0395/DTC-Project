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
from django.utils.dateparse import parse_datetime
#################################
import pandas as pd
import os
import csv
from django.conf import settings
from django.utils.text import slugify
from io import StringIO
from django.core.files import File
from django.http import HttpResponse, StreamingHttpResponse
#########################################################################
### cfehome.utils.py or the root of your project conf

def get_model_field_names(model, ignore_fields=[]):
    '''
    ::param model is a Django model class
    ::param ignore_fields is a list of field names to ignore by default
    This method gets all model field names (as strings) and returns a list 
    of them ignoring the ones we know don't work (like the 'content_object' field)
    '''
    model_fields = model._meta.get_fields()
    model_field_names = list(set([f.name for f in model_fields if f.name not in ignore_fields]))
    return model_field_names


def get_lookup_fields(model, fields=None):
    '''
    ::param model is a Django model class
    ::param fields is a list of field name strings.
    This method compares the lookups we want vs the lookups
    that are available. It ignores the unavailable fields we passed.
    '''
    model_field_names = get_model_field_names(model)
    if fields is not None:
        '''
        we'll iterate through all the passed field_names
        and verify they are valid by only including the valid ones
        '''
        lookup_fields = []
        for x in fields:
            if "__" in x:
                # the __ is for ForeignKey lookups
                lookup_fields.append(x)
            elif x in model_field_names:
                lookup_fields.append(x)
    else:
        '''
        No field names were passed, use the default model fields
        '''
        lookup_fields = model_field_names
    return lookup_fields

def qs_to_dataset(qs, fields=None):
    '''
    ::param qs is any Django queryset
    ::param fields is a list of field name strings, ignoring non-model field names
    This method is the final step, simply calling the fields we formed on the queryset
    and turning it into a list of dictionaries with key/value pairs.
    '''
    
    lookup_fields = get_lookup_fields(qs.model, fields=fields)
    return list(qs.values(*lookup_fields))


def convert_to_dataframe(qs, fields=None, index=None):
    '''
    ::param qs is an QuerySet from Django
    ::fields is a list of field names from the Model of the QuerySet
    ::index is the preferred index column we want our dataframe to be set to
    
    Using the methods from above, we can easily build a dataframe
    from this data.
    '''
    lookup_fields = get_lookup_fields(qs.model, fields=fields)
    index_col = None
    if index in lookup_fields:
        index_col = index
    elif "id" in lookup_fields:
        index_col = 'id'
    values = qs_to_dataset(qs, fields=fields)
    df = pd.DataFrame.from_records(values, columns=lookup_fields, index=index_col)
    return df
        


#######*****************   local csv *************

BASE_DIR = settings.BASE_DIR
BASE_DIR = BASE_DIR+"/leafletwebapp"
print(BASE_DIR)
def qs_to_local_csv(qs, fields=None, path=None, filename=None):
    if path is None:
        path = os.path.join(os.path.dirname(BASE_DIR), 'csvstorage')
        if not os.path.exists(path):
            '''
            CSV storage folder doesn't exist, make it!
            '''
            os.mkdir(path)
    if filename is None:
        model_name = slugify(qs.model.__name__)
        filename = "{}.csv".format(model_name)
    filepath = os.path.join(path, filename)
    lookups = get_lookup_fields(qs.model, fields=fields)
    dataset = qs_to_dataset(qs, fields)
    rows_done = 0
    with open(filepath, 'w') as my_file:
        writer = csv.DictWriter(my_file, fieldnames=lookups)
        writer.writeheader()
        for data_item in dataset:
            writer.writerow(data_item)
            rows_done += 1
    print("{} rows completed".format(rows_done))

########################################################################################

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

    #lengthOfQuerySet = len(filtered_routes)    
    # print(filtered_routes[0].vehicle_id)
    # print(filtered_routes[0].timestamp)
    # print(filtered_routes[0].pk)
    # print(filtered_routes[leng-1].pk)
    # print ("LENGTH ",len(filtered_routes))
    #buses_points = serialize('geojson',filtered_routes)
    # print(buses_points['crs']['features'][0])
    # return buses_points 
    return filtered_routes
    #return HttpResponse(buses_points,content_type='json')


def appendTimeZone(playTime):
    playTime = str(playTime)
    timeList = playTime.split('+')
    newTime = timeList[0]+'+05:30'
    newTime = parse_datetime(newTime)
    return newTime


#####################################################
class Echo:
    """An object that implements just the write method of the file-like
    interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


def downloadCSV(qs,dataset,fields=None, path=None, filename=None):
    # if path is None:
    #     path = os.path.join(os.path.dirname(BASE_DIR), 'csvstorage')
    #     if not os.path.exists(path):
    #         '''
    #         CSV storage folder doesn't exist, make it!
    #         '''
    #         os.mkdir(path)
    #print(fields)
    if filename is None:
        model_name = slugify(qs.model.__name__)
        filename = "{}.csv".format(model_name)
    
    #fp = StringIO()
    pseudo_buffer = Echo()
    lookups = get_lookup_fields(qs.model, fields=fields)
    writer = csv.DictWriter(pseudo_buffer, fieldnames=lookups)
    writer.writeheader()
    #writer.writerow(fields)
    #print(writer.writeheader())
    #writer = csv.writer(pseudo_buffer)
    
    #filepath = os.path.join(path, filename)
    
    #dataset = qs_to_dataset(qs, fields)
    #rows_done = 0
    # with open(filepath, 'w') as my_file:
    #     writer = csv.DictWriter(my_file, fieldnames=fields)
    #     writer.writeheader()
    # for data_item in dataset:
    #     print(data_item)
    #     writer.writerow(data_item)
    #     rows_done += 1
    #stream_file = File(fp)
    #print (dataset)
    response = StreamingHttpResponse((writer.writerow(data_item) for data_item in dataset),
                                        content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
    return response        
#####################################################################

class downloadView(TemplateView):
    template_name = 'download.html'
    
    
    def get(self, request):
        downloadForm = DownloadForm()
        return render(request, self.template_name,{"downloadForm":downloadForm})
    
        
    def post(self, request):
        # current_user = request.user
        downloadForm = DownloadForm(request.POST)
        
        if downloadForm.is_valid():
            startdate = downloadForm.cleaned_data['startDate']
            #enddate = downloadForm.cleaned_data['endDateTime']
            vehicle = downloadForm.getcleanedvehicle()
            route = downloadForm.cleaned_data['route_id_f']
            
            cleanStartDate = appendTimeZone(startdate)
            # if(vehicle is None and route is None): 
            if(len(vehicle)==0 and len(route)==0): 
                messages.info(request, 'Select Vehicle or Route First')
            else:

                #json_data = getData(cleanStartDate,vehicle,route)
                #return json_data
                querySetData = getData(cleanStartDate,vehicle,route)
                lengthOfQuerySet = len(querySetData)
                #print(lengthOfQuerySet)
                if(lengthOfQuerySet == 0 ):
                    messages.info(request, 'No Data to Download for Selected Vehicles')
                else:
                    #print(list(querySetData.values('vehicle_id','trip_id','route_id','latitude','longitude','speed','timestamp')[:2]))
                    #print(querySetData[lengthOfQuerySet-1].pk)

                    ## convert to dataset
                    dataset = qs_to_dataset(querySetData, fields=['vehicle_id','trip_id','route_id','latitude','longitude','speed','timestamp','id'])
                    # print(dataset)
                    
                    ## convert to dataframe
                    df = convert_to_dataframe(querySetData, fields=['vehicle_id','trip_id','route_id','latitude','longitude','speed','timestamp','id'])
                    print(df.head())


                    qs_to_local_csv(querySetData, fields=['vehicle_id','trip_id','route_id','latitude','longitude','speed','timestamp','id'])

                   #messages.info(request, 'Data Downloaded') 
                   
                    return downloadCSV(querySetData,dataset, fields=['vehicle_id','trip_id','route_id','latitude','longitude','speed','timestamp','id'])

        return render(request, self.template_name, {'downloadForm': downloadForm})