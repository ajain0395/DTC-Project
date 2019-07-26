from django.db import models

# Create your models here.
# from datetime import datetime, timedelta
import django
from django.contrib.gis.db import models as geomodels

class Buses(models.Model):
    vehicle_id = models.CharField(max_length=100, blank=False)
    trip_id = models.IntegerField()
    route_id = models.IntegerField()
    geometry = geomodels.PointField()
    speed = models.FloatField()
    timestamp = models.DateTimeField(default=django.utils.timezone.now)

    class Meta:
        # order of drop-down list items
        ordering = ('vehicle_id','trip_id','route_id','geometry','speed','timestamp',)
        # plural form in admin view
        verbose_name_plural = 'buses'