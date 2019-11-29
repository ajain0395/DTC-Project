from django.conf.urls import url
from django.urls import path
from . import views
from .views import vehiclesonroute,updateend,updatestart,updatevehicle
# from django.views.generic import TemplateView
from .views import playBackView


app_name = 'playback'

urlpatterns = [
    url(r'^playback/$', playBackView.as_view(), name='playback'),

    url(r'^updatestart/$',updatestart,name="update-start"),
    url(r'^updateend/$',updateend,name="update-end"),
    url(r'^updatevehicle/$',updatevehicle,name="update-vehicle"),
    url(r'^vehiclesonroute/$',vehiclesonroute,name="get-vehicles-on-route"),
        # url(r'^vehiclePlayback/$', views.vehiclePlayBackView.as_view(), name='vehiclePlayback'),
    # url(r'^vehiclePlayback/(?P<args_1>[0-9]+)$', views.vehiclePlayBackView.as_view(), name='vehicle_playback_2'),
    url(r'^filtered_routes/$',views.particular_buses_multiple,name="filtered-routes"),
    # url(r'^gotoPlayback/$', TemplateView.as_view(template_name='playback.html'), name="gotoPlayback"),
]