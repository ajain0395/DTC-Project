
from django.db import models
from django.contrib.gis.db import models as geomodels


class Stops(models.Model):
    geometry = geomodels.PointField()
    stop_id = models.IntegerField(blank=False)

    stop_code = models.CharField(max_length=100, blank=False)
    stop_name = models.CharField(max_length=100, blank=False)
    latitude = models.FloatField(blank=True)
    longitude = models.FloatField(blank=True)

    class Meta:
        # order of drop-down list items
        ordering = ('stop_id','stop_code','stop_name','latitude','longitude')

        # plural form in admin view
        verbose_name_plural = 'stops'