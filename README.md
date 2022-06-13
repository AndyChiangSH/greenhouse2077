# greenhouse2077

智慧物聯網期末project - 智能控制溫室2077

## 成果展示

充滿未來科技感的智慧溫室，結合感測器和AI自動控制設備(植物燈、風扇和澆水系統)，並在網站上即時監控數據。

[展示影片](https://www.youtube.com/watch?v=OYNCjNcPJX8)

![](https://i.imgur.com/7G7WOhQ.jpg)

![](https://i.imgur.com/j9P3I9p.jpg)


## 硬體

### 所需器材
* ESP32
* DHT11 (溫溼度感測器)
* BMP280 (大氣壓力感測器)
* 土壤溼度感測器
* 繼電器
* 散熱風扇
* 抽水馬達
* 植物燈
* 冷光條

### 線路設計

![](https://i.imgur.com/0kJ3QZx.jpg)
![](https://i.imgur.com/JCekK9P.jpg)
![](https://i.imgur.com/qOBhl1O.jpg)


### 硬體程式

1. 程式碼在 `/hardware/GreenHouse2077/GreenHouse2077.ino`
2. 將程式燒錄到ESP32
3. 完成!

## 軟體

1. 下載 `/software/greenhouse2077/` 資料夾
2. 安裝所需套件

```
pip install -r requirements.txt
```

3. 啟動網頁伺服器

```
python manage.py runserver 0.0.0.0:8000
```

4. 瀏覽器開啟 http://127.0.0.1:8000/
5. 完成!

## 教案

詳情請見[PPT](https://github.com/AndyChiangSH/greenhouse2077/blob/main/PPT/GreenHouse2077_final.pptx)

## 作者

* 江尚軒 ([@AndyChiangSH](https://github.com/AndyChiangSH))
* 王思正 ([@shiro-wang](https://github.com/shiro-wang))
* 洪郁修 ([@Forcer0625](https://github.com/Forcer0625))
