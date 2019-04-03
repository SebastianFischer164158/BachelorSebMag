//DoS Test script for ESP32 --- Sends temperature pickups/etc. to a thingspeak server.
 #ifdef __cplusplus
  extern "C" {
 #endif
 
  uint8_t temprature_sens_read(); //this is for reading internal CPU temp. 
 
#ifdef __cplusplus
}
#endif
#include <ThingSpeak.h>
#include <WiFi.h>
#include <WiFiClient.h>

uint8_t temprature_sens_read();
const char* ssid     = "laptopwifi";
const char* password = "apassword1";

unsigned long channelID = 749504;
const char * myWriteAPIKey = "WYBMSDVMHGQ3K901"; 

const int postingInterval = 20 * 1000; // posting interval 20s.

WiFiClient client;

void ThingSpeakUpload(int field, int value){
  ThingSpeak.setField(field,value);
  //ThingSpeak.setField(2,closecounter);
  ThingSpeak.writeFields(channelID, myWriteAPIKey); //get from Thingspeak
}

void setup() {
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);   
  ThingSpeak.begin(client);  // Initialize ThingSpeak
  // We start by connecting to a WiFi network

  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

}

void loop() {
  int internal_temp = (temprature_sens_read() - 32) / 1.8;
  Serial.print("THIS IS THE TEMPERATURE: ");
  Serial.print(internal_temp);  
  Serial.println();
  ThingSpeakUpload(3,internal_temp);
  Serial.println(WiFi.localIP());
  delay(postingInterval); //should be done with a timer. 

}
