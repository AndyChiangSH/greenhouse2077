from django.db import models

# Create your models here.
class Sensor(models.Model):
    temp = models.FloatField(verbose_name="Temperature", null=True, blank=True)
    humi = models.IntegerField(verbose_name="Humidity", null=True, blank=True)
    soil_humi = models.IntegerField(verbose_name="Soil humidity", null=True, blank=True)
    bright = models.IntegerField(verbose_name="Brightness", null=True, blank=True)
    air_p = models.FloatField(verbose_name="Air pressure", null=True, blank=True)
    time = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.time)
