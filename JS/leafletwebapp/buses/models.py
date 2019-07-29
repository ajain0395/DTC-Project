from django.db import models

# Create your models here.
# from datetime import datetime, timedelta
import django
from django.contrib.gis.db import models as geomodels

class Buses(models.Model):
    
    trip_id = models.IntegerField(blank=True)
    route_id = models.IntegerField(blank=True)
    # geometry = geomodels.PointField()
    latitude = models.FloatField(blank=True,default=0.0)
    longitude = models.FloatField(blank=True,default=0.0)
    speed = models.FloatField(blank=True)
    vehicle_id = models.CharField(max_length=100, blank=False)
    timestamp = models.DateTimeField(default=django.utils.timezone.now)

    class Meta:
        # order of drop-down list items
        ordering = ('vehicle_id','trip_id','route_id','latitude','longitude','speed','timestamp',)
        # plural form in admin view
        verbose_name_plural = 'buses'