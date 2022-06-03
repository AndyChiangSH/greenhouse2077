import csv
import random

with open('greenhouse.csv', 'w', newline='', encoding="big5") as csvfile:
    # 建立 CSV 檔寫入器
    writer = csv.writer(csvfile)
    # 寫入一列資料
    writer.writerow(["temp", "humi", "soil_humi", "bright", "air_p", "label"])
    
    temp = random.randint(10, 40)
    humi = random.randint(0, 100)
    soil_humi = random.randint(1300, 2100)
    bright = random.randint(0, 2000)
    air_p = random.randint(1000, 2000)
    
    for i in range(100):
        writer.writerow([temp, humi, soil_humi, bright, air_p, random.randint(0, 1)])
