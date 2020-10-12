/**********************************************
 * Catalin Batrinu bcatalin@gmail.com 
 * Read temperature and pressure from BMP280
 * and send it to thingspeaks.com
**********************************************/

#include <Wire.h>
#include <SPI.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BMP280.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>


#define BMP_SCK 13
#define BMP_MISO 12
#define BMP_MOSI 11 
#define BMP_CS 10

Adafruit_BMP280 bme; // I2C

const char* ssid = "FingerWeg";
const char* password = "Brass!ca290995";
const char* server = "192.168.50.25";
WiFiClient client;


/**************************  
 *   S E T U P
 **************************/
void setup() {
  Serial.begin(9600);
  Serial.println(F("BMP280 test"));
  
  if (!bme.begin()) {  
    Serial.println("Could not find a valid BMP280 sensor, check wiring!");
    while (1);
  }
  WiFi.begin(ssid, password);
  
  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) 
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");  
}

  /**************************  
 *  L O O P
 **************************/
void loop() {
    Serial.print("T=");
    Serial.print(bme.readTemperature());
    Serial.print(" *C");
    
    Serial.print(" P=");
    Serial.print((int)bme.readPressure());
    Serial.print(" Pa");

    Serial.print(" A= ");
    Serial.print(bme.readAltitude(1015.04)); // this should be adjusted to your local forcase
    Serial.println(" m");
    
    if(WiFi.status()== WL_CONNECTED){  
     
       HTTPClient http;    
       StaticJsonDocument<200> doc;
       JsonObject object  = doc.to<JsonObject>();
       object["value"] = bme.readTemperature();
       String json;
       serializeJson(doc, json);
       Serial.println("JSON");
       Serial.println(json);

       http.begin("http://192.168.50.25:5000/co2/ZuHause02");
       http.addHeader("Content-Type", "application/json");//Specify request destination
     
       int httpCode = http.POST(json);   //Send the request
       String payload = http.getString();                  //Get the response payload
     
       Serial.println(httpCode);   //Print HTTP return code
       Serial.println(payload);    //Print request response payload
     
       http.end();  //Close connection
    }
    //every 20 sec   
    delay(10000);
}