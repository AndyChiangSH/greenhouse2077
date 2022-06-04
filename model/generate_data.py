import csv
import random

with open('./model/data.csv', 'w', newline='', encoding="big5") as csvfile:
    # 建立 CSV 檔寫入器
    writer = csv.writer(csvfile)
    # 寫入一列資料
    writer.writerow(["temp", "humi", "soil_humi", "bright", "air_p", "light", "fan", "water"])
    
    for i in range(1000):
        temp = random.uniform(15, 40)
        humi = random.randint(0, 100)
        soil_humi = random.randint(1200, 2200)
        bright = random.randint(0, 3000)
        air_p = random.uniform(900, 1200)
        
        if bright >= 1500:
            light = 0
        else:
            light = 1
            
        if temp >= 27:
            fan = 1
        else:
            fan = 0
        
        if soil_humi >= 1900:
            water = 1
        elif soil_humi < 1500:
            water = 0
        else:
            water = 2
        
        writer.writerow([temp, humi, soil_humi, bright, air_p, light, fan, water])
