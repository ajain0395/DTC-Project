from django.conf.urls import url
from django.views.generic import TemplateView
from .views import (AllStops,
StopsDetailView,
StopsTemplateView,
BusesDetailView,
particular_bus_id,
HomePageView)


app_name = 'stops'

urlpatterns = [
    # stops detail view
    url(r'^(?P<pk>[0-9]+)$',
        StopsDetailView.as_view(), name='stops-detail'),

            url(r'^buses/(?P<pk>[0-9]+)$',
        BusesDetailView.as_view(), name='buses-detail'),

        url(r'^allstops/$',
        AllStops,name="all-stops"),

        url(r'^all_buses/$',
        HomePageView.all_buses_data,name="all-buses"),
        
        url(r'^line_buses/$',    
        HomePageView.bus_route_line_data,name="line-buses"),


        url(r'^$',HomePageView.as_view(),name="homepage"),

        url(r'^allbuses/(?P<vehicle_id>[0-9|a-z|A-Z]+)$',
        particular_bus_id,name="particular-bus"),


        
        url(r'^filtered_buses/$',
        HomePageView.particular_buses_multiple,name="filtered-buses"),
]