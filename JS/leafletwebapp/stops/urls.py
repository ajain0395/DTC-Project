from django.conf.urls import url
from . import views


app_name = 'stops'

urlpatterns = [
    # stops detail view
    url(r'^stops/(?P<pk>[0-9]+)$',
        views.StopsDetailView.as_view(), name='stops-detail'),
]