# from django.db import models
# from django.contrib.gis.db import models as geomodels
# from django.db.models import Manager as GeoManager
# import django

# # Create your models here.
# class Buses(models.Model):
    
#     trip_id = models.IntegerField(blank=True)
#     route_id = models.IntegerField(blank=True)
#     geometry = geomodels.PointField(srid=4326,blank=True)
#     latitude = models.FloatField(blank=True,default=0.0)
#     longitude = models.FloatField(blank=True,default=0.0)
#     speed = models.FloatField(blank=True)
#     vehicle_id = models.CharField(max_length=100, blank=False)
#     timestamp = models.DateTimeField(blank=True)

#     class Meta:
#         # order of drop-down list items
#         ordering = ('vehicle_id','trip_id','route_id','latitude','longitude','speed','timestamp','geometry')
#         # plural form in admin view
#         verbose_name_plural = 'buses'