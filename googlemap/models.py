# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.contrib.gis.db import models

class Cityinfo(models.Model):
    cityname = models.CharField(max_length=80, blank=True,primary_key=True)
    countryname = models.CharField(max_length=80, blank=True)
    populationclass = models.CharField(max_length=80, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)

    geom = models.PointField()
    objects = models.GeoManager()
    class Meta:
        db_table = 'cityinfo'

#    def __unicode__(self):
#       return self.cityname
