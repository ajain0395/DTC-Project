from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import Stops

@admin.register(Stops)
class StopAdmin(OSMGeoAdmin):
    list_display = ('stop_name', 'longitude','latitude','geometry')
# admin.site.register(Stops,StopAdmin)