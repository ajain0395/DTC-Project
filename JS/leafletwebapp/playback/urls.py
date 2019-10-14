from django.conf.urls import url
from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = 'playback'

urlpatterns = [
    url(r'^playback/$', views.playBackView.as_view(), name='playback'),
    url(r'^filtered_routes/$',views.particular_buses_multiple,name="filtered-routes"),
    # url(r'^gotoPlayback/$', TemplateView.as_view(template_name='playback.html'), name="gotoPlayback"),
]