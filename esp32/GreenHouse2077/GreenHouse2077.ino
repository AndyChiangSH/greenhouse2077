#include <Wire.h>
#include <SPI.h>
#include <Adafruit_BMP280.h>
#include <SimpleDHT.h>
#include <Timer.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <Arduino_JSON.h>

#define BMP_SCK  (13)
#define BMP_MISO (12)
#define BMP_MOSI (11)
#define BMP_CS   (10)
#define soilread 32
#define watering 23
#define pinDHT11 33
#define fan 19
#define sensor_light 35
#define control_light 18
#define SensorDelay 10000
#define DeviceDelay 2000
#define water_up 3000
#define water_down 2400

#define Connected 1
#define Unconnected 0
#define ON 1
#define OFF 0

Timer t1, t2;

float BMP_temp = 10.0;
float BMP_airp = 20.0;
byte DHT_temp = 30;
byte DHT_humi = 40;
int soil_humi = 50;
int light = 60;

int Web_connect = Unconnected;
int Web_light = OFF;
int Web_water = OFF;
int Web_fan = OFF;
int Local_light = OFF;
int Local_water = OFF;
int Local_fan = OFF;

SimpleDHT11 dht11(pinDHT11);
Adafruit_BMP280 bmp; // I2C
//Adafruit_BMP280 bmp(BMP_CS); // hardware SPI
//Adafruit_BMP280 bmp(BMP_CS, BMP_MOSI, BMP_MISO,  BMP_SCK);

const char* ssid = "<你的Wifi名稱>";
const char* password = "<你的Wifi密碼>";
String serverName = "<你的IP位置和port>";

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
    pinMode(sensor_light, INPUT);
    pinMode(control_light, OUTPUT);
    
    t1.every(SensorDelay, api_sensor);
    t2.every(DeviceDelay, api_device);

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
    Serial.print(F("Temperature = "));
    Serial.print(bmp.readTemperature());
    Serial.println(" *C");
    BMP_temp = bmp.readTemperature();
    Serial.print(F("Pressure = "));
    Serial.print(bmp.readPressure());
    Serial.println(" Pa");
    BMP_airp = bmp.readPressure();
    Serial.print(F("Approx altitude = "));
    Serial.print(bmp.readAltitude(1013.25)); /* Adjusted to local forecast! */
    Serial.println(" m");
    
    //soil
    soil_humi=analogRead(soilread); //讀取感測器回傳值
    Serial.print("value:");
    Serial.println(soil_humi);
    if ((int)soil_humi > water_up){
      Local_water = ON;
      //digitalWrite(watering, LOW);
      //Serial.println("開啟"); 
    }else if((int)soil_humi < water_down){
      Local_water = OFF;
      //digitalWrite(watering, HIGH);
      //Serial.println("關閉");
    }
    //light
    light = analogRead(sensor_light);
    Serial.print("light="); Serial.println(light);  //兩顆電阻串聯
    if((int)light > 1500){
      Local_light = OFF;
      //digitalWrite(control_light, HIGH);
    }else{
      Local_light = ON;
      //digitalWrite(control_light, LOW);
    }
    //dht
    int err = SimpleDHTErrSuccess;
    if ((err = dht11.read(&DHT_temp, &DHT_humi, NULL)) != SimpleDHTErrSuccess) {
      Serial.print("Read DHT11 failed, err="); 
      Serial.println(err); 
      delay(1000);
    }
    Serial.print("temp="); Serial.print((int)DHT_temp);  // 印出溫度
    Serial.print(", humi="); Serial.print((int)DHT_humi);   // 印出濕度
    Serial.println();
    if((int)DHT_temp >= 27 ){
      Local_fan = ON;
      //digitalWrite(fan, LOW);
    }else{
      Local_fan = OFF;
      //digitalWrite(fan, HIGH);
    }
    
    //device_control
    if(Web_connect){
      if(Web_light){
        digitalWrite(control_light, LOW);
      }else{
        digitalWrite(control_light, HIGH);  
      }
      if(Web_water){
        digitalWrite(watering, LOW);
      }else{
        digitalWrite(watering, HIGH);  
      }
      if(Web_fan){
        digitalWrite(fan, LOW);
      }else{
        digitalWrite(fan, HIGH);  
      }
    }else{
      if(Local_light){
        digitalWrite(control_light, LOW);
      }else{
        digitalWrite(control_light, HIGH);  
      }
      if(Local_water){
        digitalWrite(watering, LOW);
      }else{
        digitalWrite(watering, HIGH);  
      }
      if(Local_fan){
        digitalWrite(fan, LOW);
      }else{
        digitalWrite(fan, HIGH);  
      }
    }
    
    t1.update();
    t2.update();
    Serial.println("\n");
    delay(2000);
}

void api_sensor() {
    Serial.print("\n...Send Data to Server Database...\n");

    //Check WiFi connection status
    if(WiFi.status()== WL_CONNECTED){
        HTTPClient http;
  
        String serverPath = serverName + "api/sensor/?temp="+ (String)BMP_temp + "&humi="+ (String)DHT_humi +"&soil_humi="+ (String)soil_humi +"&bright="+ (String)light +"&air_p="+ (String)BMP_airp; // 接上要傳遞的參數
        
        //Serial.println("serverPath = "+serverPath);
        
        // Your Domain name with URL path or IP address with path
        http.begin(serverPath.c_str());
        Serial.println("Http GET request:"+serverPath);
        
        // Send HTTP GET request
        int httpResponseCode = http.GET();
        
        if (httpResponseCode>0) {
          Serial.print("HTTP Response code: ");
          Serial.println(httpResponseCode);
          String payload = http.getString();
          // Serial.println(payload);
          //Web_connect = Connected;
        }
        else {
          Serial.print("Error code: ");
          Serial.println(httpResponseCode);
          //Web_connect = Unconnected;
        }
        // Free resources
        http.end();
    }
    else {
        Serial.println("WiFi Disconnected");
    }
    Serial.println();
}
void api_device(){
    Serial.print("\n...Get Data From Server ...\n");

    //Check WiFi connection status
    if(WiFi.status()== WL_CONNECTED){
    HTTPClient http;

    String serverPath = serverName + "api/device/?temp="+ (String)BMP_temp + "&humi="+ (String)DHT_humi +"&soil_humi="+ (String)soil_humi +"&bright="+ (String)light +"&air_p="+ (String)BMP_airp; // 只請求response
    
    //Serial.println("serverPath = "+serverPath);
    
    // Your Domain name with URL path or IP address with path
    http.begin(serverPath.c_str());
    Serial.println("Http GET request:"+serverPath);
    
    // Send HTTP GET request
    int httpResponseCode = http.GET();
    
    if (httpResponseCode>0) {
      Serial.print("HTTP Response code: ");
      Serial.println(httpResponseCode);
      String payload = http.getString();
      Serial.println(payload);
      JSONVar deviceObject = JSON.parse(payload);
      if (JSON.typeof(deviceObject) == "undefined") {
        Serial.println("Parsing input failed!");
        return;
      }
      Serial.print("JSON object = ");
      Serial.println(deviceObject);
      Serial.print("light:"); Serial.println(deviceObject["light"]);
      Serial.print("fan:"); Serial.println(deviceObject["fan"]);
      Serial.print("water:"); Serial.println(deviceObject["water"]);
      if((int)deviceObject["light"] == 1){
        Web_light = ON;
      }else{
        Web_light = OFF;
      }
      if((int)deviceObject["fan"] == 1){
        Web_fan = ON;  
      }else{
        Web_fan = OFF;
      }
      if((int)deviceObject["water"] == 1){
        Web_water = ON;  
      }else{
        Web_water = OFF;
      }
      Web_connect = Connected;
    }
    else {
      Serial.print("Error code: ");
      Serial.println(httpResponseCode);
      Web_connect = Unconnected;
    }
    // Free resources
    http.end();
    }
    else {
        Serial.println("WiFi Disconnected");
    }
    Serial.println();
}
