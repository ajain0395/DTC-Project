from django.shortcuts import render
from django.views.generic import DetailView,TemplateView
from django.http import HttpResponseRedirect
from django.core.serializers import serialize
from django.http import HttpRequest, HttpResponse
# Create your views here.

class downloadView(DetailView):
    template_name = 'base.html'
    from stops.models import Buses
    
    def get(self, request):
         return render(request,self.template_name)