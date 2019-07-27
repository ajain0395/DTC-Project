from django.shortcuts import render
from django.views.generic import DetailView
from .models import Stops


class StopsDetailView(DetailView):
    """
        Stops detail view.
    """
    template_name = 'stops/stops-detail.html'
    model = Stops
# Create your views here.
