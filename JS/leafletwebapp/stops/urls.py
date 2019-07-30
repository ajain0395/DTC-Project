from django.conf.urls import url
from .views import AllStops,StopsDetailView,StopsTemplateView

app_name = 'stops'

urlpatterns = [
    # stops detail view
    url(r'^(?P<pk>[0-9]+)$',
        StopsDetailView.as_view(), name='stops-detail'),

        url(r'^allstops/$',
        AllStops,name="all-stops"),

        url(r'^$',
        StopsTemplateView.as_view(), name='stops-template'),
# url(r'^(?P<pk>[0-9]+)$', views.LocationsView, name='location-bus'),
]

# urlpatterns = [

# ]