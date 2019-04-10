// Imports
#include <SoftwareSerial.h>

#include "AES.h"
#include "RSA.h"

String readBluetooth(void);

void fromStringToIntarray(String, int);
void printIntArray(String, int, int);
void sendBigNumber(BigNumber);
void sendStringNumber(String);
void hexToCharAESArray(char);
void sendIntArray(int, int);

BigNumber castToBignumber(String);


// Serial declerations
SoftwareSerial BTSerial(D6, D7); // RX | TX


// Variable decleration
String msg = "Request RSAKey";
String ReceivedRSAKey;
String myString;

bool AesComm = false;
bool hi = true;

int AES_KEY[16] = {0x54, 0x48, 0x41, 0x54, 0x53, 0x20, 0x4d, 0x59, 0x20, 0x4b, 0x55, 0x4e, 0x47, 0x20, 0x46, 0x55}; //THATS MY KONG FU
int txt_to_encrypt[16] = {0};

char test[16] = "TEMPERATURERRRR";
char holdkey[33];

int txt_len = strlen(test);
int state = 0;

  


void setup()
{
  Serial.begin(9600);
  BigNumber::begin();
  delay(100);
  
  BTSerial.begin(38400);  // HC-05 default speed in AT command more
  Serial.println("Bluetooth Serial runnning correctly on SLAVE");
} // End of Setup.

void loop(){
  if (state == 0){
    delay(2500);
    Serial.println("State: 0");
    
    // Sending char array
    sendStringNumber(msg);
    Serial.print("Sending: ");
    Serial.println("RSA Request");
    
    state = 1;
  }
  if (state == 1){
    delay(2500);
    Serial.println();
    Serial.println("State: 1");
    
    ReceivedRSAKey = readBluetooth();
    Serial.print("Received RsaPublicKey: ");
    Serial.println(ReceivedRSAKey);
    
    state = 2;
  }
  if (state == 2){
    delay(2500);
    Serial.println();
    Serial.println("State: 2");
    BigNumber RSAPublicKey = castToBignumber(ReceivedRSAKey);
    
    hexToCharAESArray(holdkey);
    BigNumber AES_CONVERTED_KEY_CHAR = holdkey; //key is now converted from int array to char array and then varible set as bignumber
    BigNumber AES_ENC = Encrypt(AES_CONVERTED_KEY_CHAR,RSAPublicKey);

    // Sending encrypted AES Key
    sendBigNumber(AES_ENC);
    Serial.println("Sending: Encrypted AES Key");
    
    
    state = 3;
  }
  if (state == 3){
    delay(2500);
    Serial.println();
    Serial.println("State: 3");
    
    myString = readBluetooth();
    Serial.print("Received: ");
    Serial.println(myString);
    Serial.println();
    state = 4;
    AesComm = true;
    delay(500);
  }

  Serial.print("AES communication enabled: ");
  if (AesComm){
    Serial.println("TRUE");
  } else {
    Serial.println("FALSE");
  }
  
  if (AesComm){
    // Print integer values of what to be sent.
    fromStringToIntarray(test, txt_to_encrypt);
    printIntArray("Text to be send: ",txt_to_encrypt,16);

    // Call the encryption methoed. 
    encryption(txt_to_encrypt,AES_KEY);

    // Print encrypted message - Integer values
    sendIntArray(txt_to_encrypt, 16);
    printIntArray("Sending encrypted text: ", txt_to_encrypt, 16);
    Serial.println();
    delay(4000);
  }
delay(1000);
} // End of Loop.



String readBluetooth(){
  String temp = "";
  //ESP.wdtDisable();
  Serial.print("Waiting for Data..");
  while (temp == ""){
    Serial.print(".");
    while (BTSerial.available()) {
      delay(20);  //small delay to allow input buffer to fill
    
      char c = BTSerial.read();  //gets one byte from serial buffer
      if (c == ',') {
        break;
      }  //breaks out of capture loop to print readstring
      
      temp += c;
    }
    delay(100);
  }
  Serial.println();
  return temp;
} // End of readBluetooth



void sendBigNumber(BigNumber msg){
  BTSerial.flush();
  String MyString = msg.toString();
  for (int i = 0; i < MyString.length(); i++){
    BTSerial.write(MyString[i]);
  }
} // End of sendBigNumber.



void sendStringNumber(String msg){
  BTSerial.flush();
  for (int i = 0; i < msg.length(); i++){
    BTSerial.write(msg[i]);
  }
} // End of sendStringNumber.


void sendIntArray(int *msg, int msgSize){
  BTSerial.flush();
  for (int i = 0; i < msgSize; i++){
    BTSerial.write(msg[i]);
  }
} // End of sendBigNumber.



BigNumber castToBignumber(String msg){
  char temp[(msg.length()+1)];
  msg.toCharArray(temp, (msg.length()+1));
  return temp;
} // End of castToBignumber.



void hexToCharAESArray(char *src){
  int place = 0;
  for (int i=0; i<16; i++)
    place += sprintf(&src[place], "%d", AES_KEY[i]); //this is magic man. 
} // End of hexToCharAESArray.


void fromStringToIntarray(String src, int *dst){
  char HoldRes;
  for (int i = 0; i < 16; i++){
    HoldRes = src[i];
    dst[i] = (int) HoldRes;
  }
} // End of fromStringToIntarray


void printIntArray(String prefix, int *src, int sizeArray){
  delay(50);
  Serial.print(prefix);
  for (int i = 0; i < sizeArray; i++){
      Serial.print(src[i]);
      Serial.print(" ");
    }
    Serial.println();
} // End of printIntArray.
