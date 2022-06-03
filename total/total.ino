#include <Wire.h>
#include <SPI.h>
#include <Adafruit_BMP280.h>
#include <SimpleDHT.h>
#include <Timer.h>
#include <WiFi.h>
#include <HTTPClient.h>

#define BMP_SCK  (13)
#define BMP_MISO (12)
#define BMP_MOSI (11)
#define BMP_CS   (10)
#define soilread 2
#define watering 23
#define pinDHT11 4
#define fan 19
#define sensorlight 15
#define control_light 18

Timer t1, t2;

float BMP_temp = 0.0;
float BMP_airp = 0.0;
byte DHT_temp = 0;
byte DHT_humi = 0;
int  soil_humi;
int light = 0;

SimpleDHT11 dht11(pinDHT11);
Adafruit_BMP280 bmp; // I2C
//Adafruit_BMP280 bmp(BMP_CS); // hardware SPI
//Adafruit_BMP280 bmp(BMP_CS, BMP_MOSI, BMP_MISO,  BMP_SCK);

const char* ssid = "Andy's Laptop";
const char* password = "00000000";
String serverName = "http://192.168.0.123:8000/";

void setup() {
    Serial.begin(9600);
    //setup for pressure
    while ( !Serial ) delay(100);   // wait for native usb
    Serial.println(F("BMP280 test"));
    unsigned status;
    //status = bmp.begin(BMP280_ADDRESS_ALT, BMP280_CHIPID);
    status = bmp.begin(0x76);
    if (!status) {
      Serial.println(F("Could not find a valid BMP280 sensor, check wiring or "
                        "try a different address!"));
      Serial.print("SensorID was: 0x"); Serial.println(bmp.sensorID(),16);
      Serial.print("        ID of 0xFF probably means a bad address, a BMP 180 or BMP 085\n");
      Serial.print("   ID of 0x56-0x58 represents a BMP 280,\n");
      Serial.print("        ID of 0x60 represents a BME 280.\n");
      Serial.print("        ID of 0x61 represents a BME 680.\n");
      //while (1) delay(10);
    }
    
    /* Default settings from datasheet. */
    bmp.setSampling(Adafruit_BMP280::MODE_NORMAL,     /* Operating Mode. */
                    Adafruit_BMP280::SAMPLING_X2,     /* Temp. oversampling */
                    Adafruit_BMP280::SAMPLING_X16,    /* Pressure oversampling */
                    Adafruit_BMP280::FILTER_X16,      /* Filtering. */
                    Adafruit_BMP280::STANDBY_MS_500); /* Standby time. */
    // setup for soil
    pinMode(soilread, INPUT);
    pinMode(watering, OUTPUT);
    // setup for dht
    pinMode(fan, OUTPUT);
    //setup for light
    pinMode(sensorlight, INPUT);
    pinMode(control_light, OUTPUT);
    
    t1.every(10000, api_sensor);

    WiFi.begin(ssid, password);
    Serial.println("Connecting");
    while(WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.print(".");
    }
    Serial.println("");
    Serial.print("Connected to WiFi network with IP Address: ");
    Serial.println(WiFi.localIP());
   
    Serial.println("Timer set to 5 seconds (timerDelay variable), it will take 5 seconds before publishing the first reading.");
}

void loop() {
    t1.update();
    Serial.print(F("Temperature = "));
    Serial.print(bmp.readTemperature());
    Serial.println(" *C");

    Serial.print(F("Pressure = "));
    Serial.print(bmp.readPressure());
    Serial.println(" Pa");

    Serial.print(F("Approx altitude = "));
    Serial.print(bmp.readAltitude(1013.25)); /* Adjusted to local forecast! */
    Serial.println(" m");
    
    //soil
    soil_humi=analogRead(soilread); //讀取感測器回傳值
    Serial.print("value:");
    Serial.println(soil_humi);
    if ((int)soil_humi > 1900){
      digitalWrite(watering, LOW);
      //Serial.println("開啟");
    }else if((int)soil_humi < 1500){
       digitalWrite(watering, HIGH);
       //Serial.println("關閉");
    }
    //light
    light = analogRead(sensorlight);
    Serial.print("light="); Serial.println(light);  //兩顆電阻串聯
    if((int)light > 1500){
      digitalWrite(control_light, HIGH);
      Serial.println("ON");
    }else{
      digitalWrite(control_light, LOW);
      Serial.println("OFF");
    }
    //dht
    int err = SimpleDHTErrSuccess;
    if ((err = dht11.read(&DHT_temp, &DHT_humi, NULL)) != SimpleDHTErrSuccess) {
      Serial.print("Read DHT11 failed, err="); 
      Serial.println(err); 
      delay(1000);
      return;
    }
    Serial.print("temp="); Serial.print((int)DHT_temp);  // 印出溫度
    Serial.print(", humi="); Serial.print((int)DHT_humi);   // 印出濕度
    Serial.println();
    if((int)DHT_temp >= 27 ){
        digitalWrite(fan, LOW);
    }else{
        digitalWrite(fan, HIGH);
    }
    
    Serial.println();
    delay(2000);
}

void api_sensor() {
    Serial.println("\n\napi_sensor<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n\n");

    //Check WiFi connection status
    if(WiFi.status()== WL_CONNECTED){
        HTTPClient http;
  
        String serverPath = serverName + "api/sensor/?temp=10&humi=20&soil_humi=30&bright=40&air_p=50"; // 接上要傳遞的參數
        Serial.println("serverPath = "+serverPath);
        
        // Your Domain name with URL path or IP address with path
        http.begin(serverPath.c_str());
        Serial.print("c_str = ");
        Serial.println(serverPath.c_str());
//        http.begin("http://ptsv2.com/t/vn6tx-1654187358/post");
        
        // Send HTTP GET request
        int httpResponseCode = http.GET();
        
        if (httpResponseCode>0) {
          Serial.print("HTTP Response code: ");
          Serial.println(httpResponseCode);
          String payload = http.getString();
          Serial.println(payload);
        }
        else {
          Serial.print("Error code: ");
          Serial.println(httpResponseCode);
        }
        // Free resources
        http.end();
    }
    else {
        Serial.println("WiFi Disconnected");
    }
}
