
from django.db import models
from django.contrib.gis.db import models as geomodels
from django.db.models import Manager as GeoManager
import django
from datetime import datetime


class Stops(models.Model):
    geometry = geomodels.PointField(srid=4326,blank=True)
    stop_id = models.IntegerField(blank=False)
    stop_code = models.CharField(max_length=100, blank=False)
    stop_name = models.CharField(max_length=100, blank=False)
    latitude = models.FloatField(blank=False)
    longitude = models.FloatField(blank=False)
    objects = GeoManager()

    class Meta:
        # order of drop-down list items
        ordering = ('stop_id','stop_code','stop_name','latitude','longitude','geometry',)

        # plural form in admin view
        verbose_name_plural = 'stops'

class Buses(models.Model):
    
    trip_id = models.CharField(max_length=100, blank=False)
    route_id = models.IntegerField(db_index=True,blank=True)
    geometry = geomodels.PointField(db_index=False,srid=4326,blank=True)
    latitude = models.FloatField(blank=True,default=0.0)
    longitude = models.FloatField(blank=True,default=0.0)
    speed = models.FloatField(blank=True)
    vehicle_id = models.CharField(db_index=True,max_length=100, blank=False)
    timestamp = models.DateTimeField(db_index=True,blank=True)
    congestion = models.IntegerField(db_index=True,blank=True,default=1)
    # trip_start_time = models.DateTimeField(db_index=True,blank=True,default= datetime.now())
    class Meta:
        # order of drop-down list items
        ordering = ('vehicle_id','trip_id','route_id','latitude','longitude','speed','timestamp','geometry','congestion')
        index_together = [
            ("vehicle_id", "route_id"),
            ('route_id','timestamp'),
            ('route_id','timestamp','vehicle_id'),
            ('timestamp','vehicle_id'),
            ('timestamp','geometry'),   
        ]
        # plural form in admin view
        verbose_name_plural = 'buses'