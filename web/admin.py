from django.contrib import admin
from .models import Sensor, Device

# Register your models here.
class SensorAdmin(admin.ModelAdmin):
    list_display = ("time", "temp", "humi", "soil_humi", "bright", "air_p")
    ordering = ("-time", )

class DeviceAdmin(admin.ModelAdmin):
    list_display = ("id", "light", "fan", "water")
    
    
admin.site.register(Sensor, SensorAdmin)    
admin.site.register(Device, DeviceAdmin)