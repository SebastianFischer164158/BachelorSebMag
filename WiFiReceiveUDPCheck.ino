/////RECEIVER/SERVER UDP WIFI CODE/////
#include "WiFi.h" //This needs to be a ESP32 in order to work, does NOT work with an EPS8266, requires WiFiesp8266 library instead.
#include "WiFiUdp.h"

WiFiUDP udp;
const char *SoftAP_SSID = "ESP32SOFTAP"; //could just be declared as []
const char *SoftAP_PASS = "testpassword";
const int SoftAP_Channel = 1;
const int SoftAP_Cloak = 0;
const int SoftAP_Max_Conn= 2;
const unsigned int UDPPort = 8888; // local port to listen for UDP packets
char ReplyBuffer[] = "ACK";
IPAddress ServerIP(192,168,4,1);
IPAddress ClientIP(192,168,4,2);
#define MAX_BUFFER_SIZE 255
char packetBuffer[MAX_BUFFER_SIZE];   //Where we get the UDP data
 
void softAPConfigESP(){
  WiFi.softAP(SoftAP_SSID,SoftAP_PASS,SoftAP_Channel,SoftAP_Cloak,SoftAP_Max_Conn);
  Serial.println();
  Serial.print("IP address of ESPWiFi: ");
  Serial.println(WiFi.softAPIP()); //should be 192.168.4.1 (this is the SoftAP IP, aka. server IP)
  Serial.print("The MAC Address of ESPWiFi: ");
  Serial.println(WiFi.macAddress());
  udp.begin(UDPPort);
}

void APSetup(){
  softAPConfigESP();
  while(WiFi.softAPgetStationNum() == 0){
    if(WiFi.softAPgetStationNum() != 0){ //this should be done in the while, but let's just make sure.
      break;
    }
  }
  Serial.print("WiFi Clients Connected : ");
  Serial.println(WiFi.softAPgetStationNum()); //we want just one client, atm.
  Serial.println();
}

String readFromClient(){
  String temp = "";
  while (temp == ""){ // Skal løbe i while loop, da vi skal læse indtil der kommer noget andet end "".
    udp.parsePacket();
    while(udp.read(packetBuffer,MAX_BUFFER_SIZE)>0){
      // We've received a UDP packet, send it to serial
      udp.read(packetBuffer, MAX_BUFFER_SIZE); // read the packet into the buffer, we are reading only one byte
      delay(20);
    }
    temp = packetBuffer;
  }
  return temp;
}

    
void setup(){
  Serial.begin(115200);
  
  // Waiting until a connection is established
  APSetup();
  int packetSize = udp.parsePacket(); //see if anything in buffer

  if (packetSize) {
    // receive incoming UDP packets
    Serial.print("Received packet from ip: ");
    Serial.println(udp.remoteIP());
    Serial.print("on port: ");
    Serial.println(udp.remotePort());


    int bufferSize = udp.read(packetBuffer, 255); // check input from app to decide action
    Serial.println(bufferSize);
  }
  

}
 
void loop(){
int packetSize = udp.parsePacket(); //see if anything in buffer

  if (packetSize) {
    // receive incoming UDP packets
    Serial.print("Received packet from ip: ");
    Serial.println(udp.remoteIP());
    Serial.print("on port: ");
    Serial.println(udp.remotePort());


    int bufferSize = udp.read(packetBuffer, 255); // check input from app to decide action
    Serial.println(bufferSize);
  }
 
}
