from django.conf.urls import url
from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = 'download'

urlpatterns = [
    url(r'^download/$', views.downloadView.as_view(), name='download'),
      
]