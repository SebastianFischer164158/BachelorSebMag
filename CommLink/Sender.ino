
#include "RSA.h"
#include "AES.h"
#include <WiFi.h>
#include <WiFiUdp.h>
#define MAX_BUFFER_SIZE 255
char packetBuffer[MAX_BUFFER_SIZE];   //Where we get the UDP data
// WiFi network name and password:
const char * networkName = "ESP32SOFTAP";
const char * networkPswd = "testpassword";
BigNumber RsaKey = 0;
//THATS MY KONG FU
int AES_KEY[16] = {0x54, 0x48, 0x41, 0x54, 0x53, 0x20, 0x4d, 0x59, 0x20, 0x4b, 0x55, 0x4e, 0x47, 0x20, 0x46, 0x55};
//IP address to send UDP data to:
// either use the ip address of the server or 
// a network broadcast address
const char * udpAddress = "192.168.4.1";
const int udpPort = 2000;

//Are we currently connected?
boolean connected = false;

//The udp library class
WiFiUDP udp;

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
  // Initilize hardware serial:
  Serial.begin(115200);
  BigNumber::begin (); //Dette *SKAL* MED!!!
  BigNumber RSA_KEY_ENCRYPTED[16];
  
  //Connect to the WiFi network
  connectToWiFi(networkName, networkPswd);
  

  //STEP 1 RECEIVE RSA KEY//
  
  while(RsaKey == 0){
    if(connected){
    //Send a packet

    udp.parsePacket();
    while(udp.read(packetBuffer,MAX_BUFFER_SIZE)>0){
    // We've received a UDP packet, send it to serial
    udp.read(packetBuffer, MAX_BUFFER_SIZE); // read the packet into the buffer, we are reading only one byte
    
    delay(20);
    }
   
    RsaKey = packetBuffer;
    Serial.println(RsaKey);

    udp.beginPacket(udpAddress,udpPort); //for whatever reason we need to begin an empty packet and end it??? why?
    //udp.print();
    udp.endPacket();
       
   
  }
  
  //Wait for 0.1 second
  delay(10);
  }
  udp.beginPacket(udpAddress,udpPort);
  udp.printf("RsaKey ACK");
  udp.endPacket();
  //STEP 2 ENCRYPT AES KEY WITH RSA PUBLIC KEY//
  /*
  for(int i = 0; i<16; i++){
    RSA_KEY_ENCRYPTED[i] = Encrypt(AES_KEY[i], RsaKey); //(BigNumber) AES_KEY[i]
  }
  printArrayBigNumb(RSA_KEY_ENCRYPTED,16);
  //
  */
  Serial.println("I AM HERE : ");
  char holdkey[33];
  int place = 0;
  for (int i=0; i<16; i++)
    place += sprintf(&holdkey[place], "%d", AES_KEY[i]); //this is magic man. 

  BigNumber AES_CONVERTED_KEY_CHAR = holdkey; //key is now converted from int array to char array and then varible set as bignumber
  BigNumber AES_ENC = Encrypt(AES_CONVERTED_KEY_CHAR,RsaKey);
  
  udp.beginPacket(udpAddress,udpPort);
  udp.print(AES_ENC);
  udp.endPacket();
  
  Serial.println("SENT ENCRYPTED AES KEY TO RECEIVER");

  Serial.println("AWAITING ACK FROM RECEIVER");
  Serial.println();

  for(int i = 0; i<MAX_BUFFER_SIZE;i++){
    packetBuffer[i] = 0;
  }
  
    
   Serial.print("I RECEIVED : ");
   
    String ACK = readFromClient();
    Serial.println(ACK);
  
  
 
}

void loop(){
  //only send data when connected
  

}

void connectToWiFi(const char * ssid, const char * pwd){
  Serial.println("Connecting to WiFi network: " + String(ssid));

  // delete old config
  WiFi.disconnect(true);
  //register event handler
  WiFi.onEvent(WiFiEvent);
  
  //Initiate connection
  WiFi.begin(ssid, pwd);

  Serial.println("Waiting for WIFI connection...");
}

//wifi event handler
void WiFiEvent(WiFiEvent_t event){
    switch(event) {
      case SYSTEM_EVENT_STA_GOT_IP:
          //When connected set 
          Serial.print("WiFi connected! IP address: ");
          Serial.println(WiFi.localIP());  
          //initializes the UDP state
          //This initializes the transfer buffer
          udp.begin(WiFi.localIP(),udpPort);
          connected = true;
          break;
      case SYSTEM_EVENT_STA_DISCONNECTED:
          Serial.println("WiFi lost connection");
          connected = false;
          break;
    }
}
