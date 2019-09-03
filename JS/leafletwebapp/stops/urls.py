from django.conf.urls import url
from django.views.generic import TemplateView
from .views import (AllStops,StopsDetailView,StopsTemplateView,AllBuses,BusesDetailView,
particular_bus_id,particular_bus_id,add_bus_to_list,particular_buses_multiple,HomePageView)

app_name = 'stops'

urlpatterns = [
    # stops detail view
    url(r'^(?P<pk>[0-9]+)$',
        StopsDetailView.as_view(), name='stops-detail'),

            url(r'^buses/(?P<pk>[0-9]+)$',
        BusesDetailView.as_view(), name='buses-detail'),

        url(r'^allstops/$',
        AllStops,name="all-stops"),

        url(r'^allbuses/$',
        AllBuses,name="all-buses"),

        # url(r'^$',
        # StopsTemplateView.as_view(), name='stops-template'),

        url(r'^$',HomePageView.as_view()),
        # url(r'^$',TemplateView.as_view(template_name = 'stops-detail.html')),

        url(r'^allbuses/(?P<vehicle_id>[0-9|a-z|A-Z]+)$',
        particular_bus_id,name="particular-bus"),

        url(r'^showbus/(?P<vehicle_id>[0-9|a-z|A-Z]+)$',
        add_bus_to_list,name="add-bus-to-list"),
        
        url(r'^filtered_buses/$',
        particular_buses_multiple,name="filtered-buses"),

        
# url(r'^(?P<pk>[0-9]+)$', views.LocationsView, name='location-bus'),
]

# urlpatterns = [

# ]