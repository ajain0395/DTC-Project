from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'playback'

urlpatterns = [
    url(r'^playback/$', views.playBackView.as_view(), name='playback'),

]