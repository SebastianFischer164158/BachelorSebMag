 #ifdef __cplusplus
  extern "C" {
 #endif
 
  uint8_t temprature_sens_read(); //this is for reading internal CPU temp. 
 
#ifdef __cplusplus
}
#endif

#include "RSA.h"
#include "AES.h"
#include "WiFi.h"
#include "WiFiUdp.h"
#define MAX_BUFFER_SIZE 255
char packetBuffer[MAX_BUFFER_SIZE];   //Where we get the UDP data

// WiFi network name and password:
const char * networkName = "ESP32SOFTAP";
const char * networkPswd = "testpassword";
BigNumber RsaKey = 0;

//THATS MY KONG FU
int AES_KEY[16] = {0x54, 0x48, 0x41, 0x54, 0x53, 0x20, 0x4d, 0x59, 0x20, 0x4b, 0x55, 0x4e, 0x47, 0x20, 0x46, 0x55};
uint8_t temprature_sens_read();
//IP address to send UDP data to:
// either use the ip address of the server or 
// a network broadcast address
const char * udpAddress = "192.168.4.1";
const int udpPort = 2000;

//Are we currently connected?
boolean connected = false;

//The udp library class
WiFiUDP udp;


// Methods below
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


//Wifi event handler
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

// Cast string to BigNumber
BigNumber castToBignumber(String msg){
  char temp[(msg.length()+1)];
  msg.toCharArray(temp, (msg.length()+1));
  return temp;
}

void clearBuffer(){
  for(int i = 0; i < MAX_BUFFER_SIZE; i++)
    packetBuffer[i] = 0;
}

void hexToCharArray(char *src){
  int place = 0;
  for (int i=0; i<16; i++)
    place += sprintf(&src[place], "%d", AES_KEY[i]); //this is magic man. 
}

void sendStringPacket(String msg){
  udp.beginPacket(udpAddress,udpPort);
  udp.print(msg);
  udp.endPacket();
}

void CompleteKeySetup(){
  //STEP 1 RECEIVE RSA KEY//
  Serial.println("i am here");
  String RsaKeyString = readFromClient();
  RsaKey = castToBignumber(RsaKeyString);
  Serial.println(RsaKey);

  // TODO Check om vi kan slette dette
  udp.beginPacket(udpAddress,udpPort); //for whatever reason we need to begin an empty packet and end it??? why?
  udp.endPacket();
  
  //Wait for 0.01 second
  delay(10);

  sendStringPacket("RsaKey ACK");
  
  //STEP 2 ENCRYPT AES KEY WITH RSA PUBLIC KEY//
  char holdkey[33];
  hexToCharArray(holdkey);

  BigNumber AES_CONVERTED_KEY_CHAR = holdkey; //key is now converted from int array to char array and then varible set as bignumber
  BigNumber AES_ENC = Encrypt(AES_CONVERTED_KEY_CHAR,RsaKey);
  
  udp.beginPacket(udpAddress,udpPort);
  udp.print(AES_ENC);
  udp.endPacket();
  
  Serial.println("SENT ENCRYPTED AES KEY TO RECEIVER");
  Serial.println("AWAITING ACK FROM RECEIVER");
  Serial.println();

  clearBuffer();
 
  Serial.print("I RECEIVED : "); 
  String ACK = readFromClient();
  Serial.println(ACK);
}

void setup(){
  // Initilize hardware serial:
  Serial.begin(115200);
  BigNumber::begin (); //Dette *SKAL* MED!!!
  BigNumber RSA_KEY_ENCRYPTED[16];
 
  // Connect to the WiFi network
  connectToWiFi(networkName, networkPswd);

  // After WiFi connection established, make key setup.

    CompleteKeySetup();

    //the message we want to sent, simple scenario//
    //SECRET MESSAGE 1
    //53 45 43 52 45 54 20 4d 45 53 53 41 47 45 20 31 (this is hex)
    //83 69 67 82 69 84 32 77 69 83 83 65 71 69 32 49 (this is decimal)
    char *test = "SECRET";
    int text_to_encrypt_aes[16] = {0};
    int txt_len = strlen(test);
    for(int z = 0; z<txt_len;z++){
      text_to_encrypt_aes[z] = (int) test[z];
    }
    encryption(text_to_encrypt_aes,AES_KEY);

    for(int k = 0; k<16;k++){
      Serial.println(text_to_encrypt_aes[k]);
    }
    
   
    udp.beginPacket(udpAddress,udpPort);
    for(int j = 0; j<16; j++){
    udp.write(text_to_encrypt_aes[j]);
    }
    
    udp.endPacket();   
  
}

void loop(){
  
  // Convert raw temperature in F to Celsius degrees
  int internal_temp = (temprature_sens_read() - 32) / 1.8;
  Serial.print("THIS IS THE TEMPERATURE: ");
  Serial.print(internal_temp);  
  Serial.println();
  char *test = "TEMPERATURE";
  int txt_to_encrypt[16] = {0};
  int txt_len = strlen(test);
  for(int z = 0; z<txt_len;z++){
      txt_to_encrypt[z] = (int) test[z];
    } 
  txt_to_encrypt[15] = internal_temp;
  encryption(txt_to_encrypt,AES_KEY);
  
    udp.beginPacket(udpAddress,udpPort);
    for(int j = 0; j<16; j++){
    udp.write(txt_to_encrypt[j]);
    }
    
    udp.endPacket();
  
  
  
  delay(5000);
  

}
