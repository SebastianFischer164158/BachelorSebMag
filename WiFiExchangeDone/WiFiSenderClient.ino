 #ifdef __cplusplus
  extern "C" {
 #endif
 
  uint8_t temprature_sens_read(); //this is for reading the internal CPU temp. 
 
#ifdef __cplusplus
}
#endif

#include <Wire.h> 
#include <LiquidCrystal_I2C.h>
#include "RSA.h"
#include "AES.h"
#include "WiFi.h"
#include "WiFiUdp.h"
//The udp library class
WiFiUDP udp;
#define MAX_BUFFER_SIZE 350
char standard_packet_buffer[MAX_BUFFER_SIZE]; //Buffer for the UDP packets 

// LCD Display
LiquidCrystal_I2C lcd(0x27, 16, 2);

// WiFi network name and password:
const char * networkName = "ESP32SOFTAP";
const char * networkPswd = "testpassword";
BigNumber RsaKey = 0;

//"THATS MY KONG FU"
//translated to hexadecimal as our key. 
//84 72 65 84 83 32 77 89 32 75 85 78 71 32 70 85
int AES_KEY[16] = {0x54, 0x48, 0x41, 0x54, 0x53, 0x20, 0x4d, 0x59, 0x20, 0x4b, 0x55, 0x4e, 0x47, 0x20, 0x46, 0x55};
uint8_t temprature_sens_read();
//UDP address we wish to send to, in this case the server. 
const char * udpAddress = "192.168.4.1";
const int udpPort = 2000;

//connection status:
boolean connected = false;

//Prototype declarations
String readFromClient(void);
void connectToWiFi(const char*, const char*);
void WiFiEvent(WiFiEvent_t);
BigNumber castToBigNumber(String);
void clearBuffer(void);
void hexToCharArray(char*);
void sendStringPacket(String);
void CompleteKeySetup(void);

////////// SETUP //////////

void setup(){
  //Initialize serial
  Serial.begin(115200);
  
  lcd.begin();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("Booting System");
  
  BigNumber::begin (); //Calling BigNumber library with c++ 
  BigNumber RSA_KEY_ENCRYPTED[16];
 
  // Connect to the WiFi network
  connectToWiFi(networkName, networkPswd);
  delay(1000);
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Connected to WIFI.");

  // After WiFi connection established, do the key setup.

    CompleteKeySetup();

    //the message we want to sent//
    //SECRET MESSAGE 1
    //53 45 43 52 45 54 20 4d 45 53 53 41 47 45 20 31 (this is hex)
    //83 69 67 82 69 84 32 77 69 83 83 65 71 69 32 49 (this is decimal)
    //char *test = "SECRET"; if len(msg) < 16, it will be zeros. 

    delay(1000);
    
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("I will start");
    lcd.setCursor(0, 1);
    lcd.print("data in: 3");

    delay(1000);

    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("I will start");
    lcd.setCursor(0, 1);
    lcd.print("data in: 2");

    delay(1000);

    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("I will start");
    lcd.setCursor(0, 1);
    lcd.print("data in: 1");

    delay(1000);

    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("I will start");
    lcd.setCursor(0, 1);
    lcd.print("data in: 0");
}

////////// MAIN LOOP //////////

void loop(){
  
  // Convert internal CPU core temp (F) to C
  //int internal_temp = (temprature_sens_read() - 32) / 1.8;
  int internal_temp = random(0,100);
  Serial.print("THIS IS THE TEMPERATURE: ");
  Serial.print(internal_temp);  
  Serial.println();
  char *test = "TEMPERATURE";
  int txt_to_encrypt[16] = {0};
  int txt_len = strlen(test);
  /*
  for(int z = 0; z<txt_len;z++){
      txt_to_encrypt[z] = (int) test[z];
    }
  */ 
  txt_to_encrypt[15] = internal_temp;
  encryption(txt_to_encrypt,AES_KEY);
  
  udp.beginPacket(udpAddress,udpPort);
  for(int j = 0; j<16; j++){
  udp.write(txt_to_encrypt[j]);
  }
  udp.endPacket();
  udp.flush();

  delay(1000);
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Sending:");
  lcd.setCursor(0, 1);
  lcd.print(internal_temp);
  
  //delay(5000);
  delay(1000); //for wireshark traces

}


////////// FUNCTIONS //////////

String readFromClient(){
  String temp = "";
  while (temp == ""){ // Skal løbe i while loop, da vi skal læse indtil der kommer noget andet end "".
    udp.parsePacket();
    while(udp.read(standard_packet_buffer,MAX_BUFFER_SIZE)>0){
      // We've received a UDP packet, send it to serial
      udp.read(standard_packet_buffer, MAX_BUFFER_SIZE); // read the packet into the buffer, we are reading only one byte
      delay(20);
    }
    temp = standard_packet_buffer;
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
  //WPA2 PSK
  //WiFi.begin(ssid, pwd);
  //open network (no password)
  WiFi.begin(ssid);

  Serial.println("Waiting for WIFI connection...");
  Serial.print("The MAC Address of ESP Client: ");
  Serial.println(WiFi.macAddress());
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
    standard_packet_buffer[i] = 0;
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

  delay(1000);
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Waiting for");
  lcd.setCursor(0, 1);
  lcd.print("RSA public Key");
  
  String RsaKeyString = readFromClient();
  RsaKey = castToBignumber(RsaKeyString);
  Serial.println(RsaKey);

  // TODO Check om vi kan slette dette
  udp.beginPacket(udpAddress,udpPort); //for whatever reason we need to begin an empty packet and end it??? why?
  udp.endPacket();
  
  //Wait for 0.01 second
  delay(10);

  sendStringPacket("RsaKey ACK");
  
  delay(1000);
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Sending RSA Ack");
  
  //STEP 2 ENCRYPT AES KEY WITH RSA PUBLIC KEY//
  char holdkey[33];
  hexToCharArray(holdkey);

  BigNumber AES_CONVERTED_KEY_CHAR = holdkey; //key is now converted from int array to char array and then varible set as bignumber
  BigNumber AES_ENC = Encrypt(AES_CONVERTED_KEY_CHAR,RsaKey);

  delay(1000);
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Send Encrypted");
  lcd.setCursor(0, 1);
  lcd.print("AES Key");
  
  udp.beginPacket(udpAddress,udpPort);
  udp.print(AES_ENC);
  udp.endPacket();
  
  Serial.println("SENT ENCRYPTED AES KEY TO RECEIVER");
  Serial.println("AWAITING ACK FROM RECEIVER");
  Serial.println();

  clearBuffer();

  delay(1000);
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Foe decrypting");
  lcd.setCursor(0, 1);
  lcd.print("Waiting for ack");
  
  Serial.print("I RECEIVED : "); 
  String ACK = readFromClient();
  Serial.println(ACK);

  delay(1000);
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Received ACK");
}
