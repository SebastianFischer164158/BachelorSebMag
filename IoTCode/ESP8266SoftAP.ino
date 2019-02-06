#include <ESP8266WiFi.h>
#include <elapsedMillis.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
elapsedMillis timeElapsed;

int interval = 2000;
const char ssid[] = "dank"; //max 31 characters
const char pass[]= "ledank"; //least 8 characters, max 63, configured with WPA2-PSK
const int channel = 1;
const int ssid_hidden = 0;

void setup()
{
  Serial.begin(115200);
  Serial.println();



  Serial.print("Setting soft-AP ... ");
  WiFi.mode(WIFI_AP);
  WiFi.softAP(ssid, "nothingyoucanfindout", 1, 0);
  Serial.println(WiFi.softAPIP());
}

void loop() {
  if(timeElapsed >= interval){
    Serial.printf("Stations connected to soft-AP = %d\n", WiFi.softAPgetStationNum());
    timeElapsed = 0;
  }
  

  
  
  }
