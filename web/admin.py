from django.contrib import admin
from .models import Sensor

# Register your models here.
class SensorAdmin(admin.ModelAdmin):
    list_display = ("time", "temp", "humi", "soil_humi", "bright", "air_p")
    ordering = ("-time", )
    
admin.site.register(Sensor, SensorAdmin)