/////RECEIVER/SERVER UDP WIFI CODE/////
#include "RSA.h"
#include "AES.h"
#include "WiFi.h"
#include "WiFiUdp.h"
//The udp library class
WiFiUDP udp;

//Buffer setup for, receiving. 
#define MAX_BUFFER_SIZE 350
#define MAX_AES_BUFFER_SIZE 16
char standard_packet_buffer[MAX_BUFFER_SIZE];   //Where we get the UDP data
char AES_packet_buffer[MAX_AES_BUFFER_SIZE];

//WiFi information for the setup. 
const char *SoftAP_SSID = "ESP32SOFTAP";
const char *SoftAP_PASS = "testpassword";
const int SoftAP_Channel = 1;
const int SoftAP_Cloak = 0;
const int SoftAP_Max_Conn = 3;

// local port to listen for UDP packets
const unsigned int UDPPort = 2000;
char ReplyBuffer[] = "ACK";

//IP-addresses declarations. 
IPAddress ServerIP(192,168,4,1);
IPAddress ClientIP(192,168,4,2);

//AES KEY Receive
int AES_KEY_RECEIVED[16] = {0};


String encAesMsg = "";
int AES_TEMP_HOLD[16] = {0};
boolean test = true;

//Prototype declarations
void softAPConfigESP(void);
void APSetup(void);
String readFromClient(void);
String readFromClientAES(void);
void sendBignumberPacket(BigNumber);
void Clear_Buffers(char*, int);
BigNumber castToBignumber(String);
void fromBignumberToIntarray(BigNumber,int*);
void fromStringToIntarray(String,int *);
void CompleteKeySetup(void);
void intArrayToString(int*);

////////// SETUP //////////
void setup(){
  Serial.begin(115200);
  BigNumber::begin();
  
  // Waiting until a connection is established
  APSetup();
  
  // RSA and AES key exchange
  CompleteKeySetup();
}

////////// MAIN LOOP //////////

void loop(){
  if (WiFi.softAPgetStationNum() != 0){
    encAesMsg = readFromClientAES();
    Serial.print("Encrypted message:  ");
    fromStringToIntarray(encAesMsg,AES_TEMP_HOLD);
    intArrayToString(AES_TEMP_HOLD);
  
    Serial.print("Decrypted message:  ");
    decryption(AES_TEMP_HOLD, AES_KEY_RECEIVED);
    for(int i = 0; i<16;i++){
      Serial.print(AES_TEMP_HOLD[i]);
      Serial.print(" ");
    }
    Serial.println();
    intArrayToString(AES_TEMP_HOLD); // This is print the decrypted input as string
    Serial.println();
  
    Clear_Buffers(AES_packet_buffer, MAX_AES_BUFFER_SIZE);
  } 
}


void softAPConfigESP(){
  //Create WiFi with WPA2 PSK
  //WiFi.softAP(SoftAP_SSID,SoftAP_PASS,SoftAP_Channel,SoftAP_Cloak,SoftAP_Max_Conn);
  //Create open WiFi (NO password)
  WiFi.softAP(SoftAP_SSID,NULL,SoftAP_Channel,SoftAP_Cloak,SoftAP_Max_Conn);
  Serial.println();
  Serial.print("IP address of ESPWiFi: ");
  Serial.println(WiFi.softAPIP()); 
  //should be 192.168.4.1 (this is the SoftAP IP, aka. server IP)
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
  Serial.println(WiFi.softAPgetStationNum()); //Client count. 
  Serial.println();
}

String readFromClient(){
  String temp = "";
  //Needs to be a while check, since we need to read untill something else than "". 
  while (temp == ""){
    udp.parsePacket();
    while(udp.read(standard_packet_buffer,MAX_BUFFER_SIZE)>0){
      udp.read(standard_packet_buffer, MAX_BUFFER_SIZE); 
      // read the packet into the buffer, we are reading only one byte
      delay(20);
    }
    temp = standard_packet_buffer;
  }
  return temp;
}


String readFromClientAES(){
  String temp = "";
  while (temp == ""){ 
    udp.parsePacket();
    while(udp.read(AES_packet_buffer,MAX_AES_BUFFER_SIZE)>0){
      udp.read(AES_packet_buffer, MAX_AES_BUFFER_SIZE);
      delay(20);
    }
    temp = AES_packet_buffer;
  }
  return temp;
}

void sendBignumberPacket(BigNumber msg){
  udp.beginPacket(ClientIP,UDPPort);
  udp.print(msg);
  udp.endPacket();
}

void Clear_Buffers(char* buffername, int sizeofbuffer){
  for(int i = 0; i < sizeofbuffer; i++){
    buffername[i] = 0;
  }
}


BigNumber castToBignumber(String msg){
  char temp[(msg.length()+1)];
  msg.toCharArray(temp, (msg.length()+1));
  return temp;
}

void fromBignumberToIntarray(BigNumber src, int *dst){
  String tempKeyHolder = src.toString();
  String HoldRes;
  for (int i = 0; i < 16; i++){
    HoldRes = "";
    HoldRes += tempKeyHolder[(i*2)];
    HoldRes += tempKeyHolder[((i*2)+1)];
    
    dst[i] = HoldRes.toInt();
  }
}

void fromStringToIntarray(String src, int *dst){
  char HoldRes;
  for (int i = 0; i < 16; i++){
    HoldRes = src[i];

    dst[i] = (int) HoldRes;
  }
}

void CompleteKeySetup(){
  // Generate RSA keys
  BigNumber publickey = PublicKeyGen();
  BigNumber privatekey = PrivateKeyGen(); //could be done at the very beginning, before serial.begin, so the calculations are done very early.
  
  //STEP 1. Send Public Key to Sender //
  Serial.println("Sending: RSA Public Key");
  udp.beginPacket(ClientIP,UDPPort);
  udp.print(publickey);
  udp.endPacket();

  // Receiving RSA key ack
  String ReceivedAck = readFromClient();
  Serial.print("Received : ");
  Serial.println(ReceivedAck);

  // Clear buffer
  Clear_Buffers(standard_packet_buffer, MAX_BUFFER_SIZE);

  // Receiving encrypted AES key.
  String encKey = readFromClient();
  BigNumber Encrypted_AES_key = castToBignumber(encKey);
  BigNumber Decrypted_AES_key = Decrypt(Encrypted_AES_key, publickey, privatekey);

  
  // Aes key as integer array
  AES_KEY_RECEIVED[16] = {0};
  fromBignumberToIntarray(Decrypted_AES_key, AES_KEY_RECEIVED);
  Serial.println("Received the following decrypted AES key:");
  for(int i = 0; i < 16; i++){
    Serial.println(AES_KEY_RECEIVED[i]);
  }
  

  // Send AES ACK
  Serial.println("Sending: AES ACK");
  
  udp.beginPacket(ClientIP,UDPPort);
  udp.printf("Aes Ack");
  udp.endPacket();

  Serial.println();
}


void intArrayToString(int *src){
  String printer;
  for (int i = 0; i < 16; i++){
    if (isAlpha((char) src[i])){
      printer += (char) src[i];
    } else {
      if (src[i] == 0)
        continue;

      if (i > 0){
        if (isAlpha(printer[(printer.length()-1)])){
          if (!(isAlpha((char)src[i]))){
            printer += ": ";
          }
        }
      }  
      printer += src[i];    
    }
  }
  Serial.println(printer);
}
