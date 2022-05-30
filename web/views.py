from logging import exception
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Device, Sensor

# Create your views here.
def index(request):
    data = Sensor.objects.all().order_by("-time")
    # print("data:", data)
    
    success = False
    temp = {"now": None, "pre": None, "diff": None}
    humi = {"now": None, "pre": None, "diff": None}
    soil_humi = {"now": None, "pre": None, "diff": None}
    bright = {"now": None, "pre": None, "diff": None}
    air_p = {"now": None, "pre": None, "diff": None}
    
    if len(data) > 0:
        success = True
        
        temp["now"] = data[0].temp
        if temp["now"] != None and len(data) > 1:
            temp["pre"] = data[1].temp
            if temp["pre"] != None:
                temp["diff"] = round(temp["now"]-temp["pre"], 1)
        
        humi["now"] = data[0].humi
        if humi["now"] != None and len(data) > 1:
            humi["pre"] = data[1].humi
            if humi["pre"] != None:
                humi["diff"] = round(humi["now"]-humi["pre"], 1)
        
        soil_humi["now"] = data[0].soil_humi
        if soil_humi["now"] != None and len(data) > 1:
            soil_humi["pre"] = data[1].soil_humi
            if soil_humi["pre"] != None:
                soil_humi["diff"] = round(soil_humi["now"]-soil_humi["pre"], 1)
                
        bright["now"] = data[0].bright
        if bright["now"] != None and len(data) > 1:
            bright["pre"] = data[1].bright
            if bright["pre"] != None:
                bright["diff"] = round(bright["now"]-bright["pre"], 1)
        
        air_p["now"] = data[0].air_p
        if air_p["now"] != None and len(data) > 1:
            air_p["pre"] = data[1].air_p
            if air_p["pre"] != None:
                air_p["diff"] = round(air_p["now"]-air_p["pre"], 1)
        
    context = {
        "success": success,
        "temp": temp,
        "humi": humi,
        "soil_humi": soil_humi,
        "bright": bright,
        "air_p": air_p,
    }
        
    return render(request, "index.html", context)


def add_data(request):
    try:
        temp = request.GET["temp"]
        humi = request.GET["humi"]
        soil_humi = request.GET["soil_humi"]
        bright = request.GET["bright"]
        air_p = request.GET["air_p"]
        
        if temp == "":
            temp = None
        if humi == "":
            humi = None
        if soil_humi == "":
            soil_humi = None
        if bright == "":
            bright = None
        if air_p == "":
            air_p = None
        
        new_data = Sensor.objects.create(temp=temp, humi=humi, soil_humi=soil_humi, bright=bright, air_p=air_p)
        new_data.save()
        
        return HttpResponse("Add data success.")
    except exception as e:
        return HttpResponse(f"Add data fail.<br>{e}")


def chart(request, name="temperature"):
    data = Sensor.objects.all().order_by("time")
    
    if name == "temperature":
        label = "Temperature"
    elif name == "humidity":
        label = "Humidity"
    elif name == "soil_humidity":
        label = "Soil humidity"
    elif name == "brightness":
        label = "Brightness"
    elif name == "air_pressure":
        label = "Air pressure"
    else:
        return redirect("/")
    
    x = list()
    y = list()
    for d in data:
        x.append(d.time.strftime("%Y/%m/%d %H:%M"))
        if name == "temperature":
            y.append(d.temp)
        if name == "humidity":
            y.append(d.humi)
        if name == "soil_humidity":
            y.append(d.soil_humi)
        if name == "brightness":
            y.append(d.bright)
        if name == "air_pressure":
            y.append(d.air_p)
    
    context = {
        "label": label,
        "x": x,
        "y": y,
    }
    
    return render(request, "chart.html", context=context)


def devices(request):
    try:
        device = Device.objects.get(id=1)
    except exception as e:
        return HttpResponse(f"Get device fail.<br>{e}")
    
    context = {
        "device": device,
    }
    
    return render(request, "devices.html", context=context)


def switch_device(request, device):
    try:
        device_data = Device.objects.get(id=1)
    except exception as e:
        return HttpResponse(f"Get device fail.<br>{e}")
    
    if device == "light":
        device_data.light = not device_data.light
    elif device == "fan":
        device_data.fan = not device_data.fan
    elif device == "water":
        device_data.water = not device_data.water
    
    device_data.save()
    return redirect("/devices/")
    