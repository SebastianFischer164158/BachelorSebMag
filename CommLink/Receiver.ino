/////RECEIVER/SERVER UDP WIFI CODE/////
#include "RSA.h"
#include "AES.h"
#include "WiFi.h" //This needs to be a ESP32 in order to work, does NOT work with an EPS8266, requires WiFiesp8266 library instead.
#include "WiFiUdp.h"
//#include "BigNumber.h" //burde ikke være nødvendigt da den allerede eksisterer
// A UDP instance to let us send and receive packets over UDP
WiFiUDP udp;
const char *SoftAP_SSID = "ESP32SOFTAP"; //could just be declared as []
const char *SoftAP_PASS = "testpassword";
const int SoftAP_Channel = 1;
const int SoftAP_Cloak = 0;
const int SoftAP_Max_Conn= 1;
const unsigned int UDPPort = 2000; // local port to listen for UDP packets
char ReplyBuffer[] = "ACK";
IPAddress ServerIP(192,168,4,1);
IPAddress ClientIP(192,168,4,2);
#define MAX_BUFFER_SIZE 255
#define MAX_AES_BUFFER_SIZE 16
char packetBuffer[MAX_BUFFER_SIZE];   //Where we get the UDP data
char packetAesBuffer[MAX_AES_BUFFER_SIZE];
 
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

String readFromClientAES(){
  String temp = "";
  while (temp == ""){ // Skal løbe i while loop, da vi skal læse indtil der kommer noget andet end "".
    udp.parsePacket();
    while(udp.read(packetAesBuffer,MAX_AES_BUFFER_SIZE)>0){
      // We've received a UDP packet, send it to serial
      udp.read(packetAesBuffer, MAX_AES_BUFFER_SIZE); // read the packet into the buffer, we are reading only one byte
      delay(20);
    }
    temp = packetAesBuffer;
  }
  return temp;
}

void sendBignumberPacket(BigNumber msg){
  udp.beginPacket(ClientIP,UDPPort);
  udp.print(msg);
  udp.endPacket();
}

void clearBuffer(){
  for(int i = 0; i < MAX_BUFFER_SIZE; i++)
    packetBuffer[i] = 0;
}

void clearAesBuffer(){
  for(int i = 0; i < MAX_AES_BUFFER_SIZE; i++)
    packetAesBuffer[i] = 0;
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

// sæt den op til de andre globale variabler
int AES_key[16] = {0};

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
  clearBuffer();

  // Receiving encrypted AES key.
  String encKey = readFromClient();
  BigNumber encAesKey = castToBignumber(encKey);
  BigNumber AesKey = Decrypt(encAesKey, publickey, privatekey);
  
  // Aes key as integer array
  AES_key[16] = {0};
  fromBignumberToIntarray(AesKey,AES_key);

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

    
void setup(){
  Serial.begin(115200);
  BigNumber::begin ();
  
  // Waiting until a connection is established
  APSetup();
  
  // RSA and AES key exchange
  CompleteKeySetup();
}


String encAesMsg = "";
int holderAes[16] = {0};
boolean test = true;

void loop(){
  if (WiFi.softAPgetStationNum() != 0){
    encAesMsg = readFromClientAES();
    Serial.print("Encrypted message:  ");
    fromStringToIntarray(encAesMsg,holderAes);
    intArrayToString(holderAes);
  
    Serial.print("Decrypted message:  ");
    decryption(holderAes, AES_key);
    intArrayToString(holderAes); // This is print the decrypted input as string
    Serial.println();
  
    clearAesBuffer();
  } 
}
