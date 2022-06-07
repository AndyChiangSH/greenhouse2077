from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from .models import Sensor
from .forms import TimeRangeForm 
import pandas as pd
import joblib
import json


AI_CONTROL = False
LIGHT_STATE = False
FAN_STATE = False
WATER_STATE = False

light_model = joblib.load('./model/light_model.joblib')
fan_model = joblib.load('./model/fan_model.joblib')
water_model = joblib.load('./model/water_model.joblib')


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


def chart(request, name="temperature"):
    form = TimeRangeForm(request.GET)
    try:
        start_time = form.data["start_time"]
        end_time = form.data["end_time"]
        data = Sensor.objects.filter(time__range=[start_time, end_time]).order_by("-time")
    except:
        data = Sensor.objects.all().order_by("-time")[:20]
    
    data = reversed(data)
    
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
        time_in_timezone = d.time+timezone.timedelta(hours=8)
        # print(time_in_timezone)
        x.append(time_in_timezone.strftime("%Y-%m-%d %H:%M"))
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
        "form": form,
    }
    
    return render(request, "chart.html", context=context)


def devices(request):
    global LIGHT_STATE, FAN_STATE, WATER_STATE
    context = {
        "light": LIGHT_STATE,
        "fan": FAN_STATE,
        "water": WATER_STATE,
        "AI_CONTROL": AI_CONTROL,
    }
    
    return render(request, "devices.html", context=context)


def switch_device(request, device):
    global LIGHT_STATE, FAN_STATE, WATER_STATE
    if device == "light":
        LIGHT_STATE = not LIGHT_STATE
    elif device == "fan":
        FAN_STATE = not FAN_STATE
    elif device == "water":
        WATER_STATE = not WATER_STATE
    
    return redirect("/devices/")


def switch_control(request):
    global AI_CONTROL
    c = request.GET["c"]
    
    if c != None:
        if c == "True":
            AI_CONTROL = True
            messages.add_message(request, messages.SUCCESS, "Open AI control!")
        else:
            AI_CONTROL = False
            messages.add_message(request, messages.WARNING, "Close AI control!")
    
    return redirect("/devices/")


# API: 接收感測器
def api_sensor(request):
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
        
        temp = round(float(temp), 2)
        humi = int(humi)
        soil_humi = int(soil_humi)
        bright = int(bright)
        air_p = round(float(air_p)/100, 2)
        print(f"temp={temp}, humi={humi}, soil_humi={soil_humi}, bright={bright}, air_p={air_p}")
        
        new_data = Sensor.objects.create(temp=float(temp), humi=humi, soil_humi=soil_humi, bright=bright, air_p=air_p)
        new_data.save()
        
        messages.add_message(request, messages.INFO, "Sensor data update successful!")
        return HttpResponse("Sensor data update successful!")
    except:
        messages.add_message(request, messages.ERROR, "Sensor data update fail!")
        return HttpResponse("Sensor data update fail!")


# API: 回傳裝置狀態
def api_device(request):
    global LIGHT_STATE, FAN_STATE, WATER_STATE
    
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
    
    temp = float(temp)
    humi = int(humi)
    soil_humi = int(soil_humi)
    bright = int(bright)
    air_p = float(air_p)/100
    
    global AI_CONTROL
    print("AI_CONTROL =", AI_CONTROL)
    if AI_CONTROL:  # AI控制
        data = {"temp": [temp], "humi": [humi], "soil_humi": [soil_humi], "bright": [bright], "air_p": [air_p]}
        df = pd.DataFrame(data=data)
        print(df)  
        
        light_pred = light_model.predict(df)
        print("light_pred =", light_pred)
        fan_pred = fan_model.predict(df)
        print("fan_pred =", fan_pred)
        water_pred = water_model.predict(df)
        print("water_pred =", water_pred)
        
        light_next = bool(light_pred[0])
        fan_next = bool(fan_pred[0])
        water_next = water_pred[0]
        
        if LIGHT_STATE != light_next:
            LIGHT_STATE = light_next
            if light_next == True:
                messages.add_message(request, messages.SUCCESS, "[AI] Light ON!")
            else:
                messages.add_message(request, messages.WARNING, "[AI] Light OFF!")
        
        if FAN_STATE != fan_next:
            FAN_STATE = fan_next
            if fan_next == True:
                messages.add_message(request, messages.SUCCESS, "[AI] Fan ON!")
            else:
                messages.add_message(request, messages.WARNING, "[AI] Fan OFF!")
        
        if water_next != 2:
            if WATER_STATE != bool(water_next):
                WATER_STATE = bool(water_next)
                if bool(water_next) == True:
                    messages.add_message(request, messages.SUCCESS, "[AI] Water ON!")
                else:
                    messages.add_message(request, messages.WARNING, "[AI] Water OFF!")
        
        # LIGHT_STATE, FAN_STATE, WATER_STATE = device_pred(temp, humi, soil_humi, bright, air_p, WATER_STATE)
        
    # 回傳json
    json_obj = {
        "light": int(LIGHT_STATE),
        "fan": int(FAN_STATE),
        "water": int(WATER_STATE),
    }
    print(json_obj)
        
    return HttpResponse(json.dumps(json_obj))
