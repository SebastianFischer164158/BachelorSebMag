// Imports
#include <SoftwareSerial.h>

#include "AES.h"
#include "RSA.h"

String readBluetooth(void);

void sendBigNumber(BigNumber);
void sendStringNumber(String);
void hexToCharAESArray(char);
void fromStringToIntarray(String, int);
void intArrayToString(int);
void fromBignumberToIntarray(BigNumber, int);
void printIntArray(String, int, int);

BigNumber castToBignumber(String);


// Serial declerations 
SoftwareSerial BTSerial(D6, D7); // RX | TX


// Variable decleration
BigNumber privatekey = 0;
BigNumber publickey = 0;
BigNumber AesKey = 0;

int state = 0;

String encAesMsg;
String myString;

bool AesComm = false;
bool runable = true;
bool hi = true;

int holderAes[16] = {0};
int AES_key[16] = {0};
char RSAKey[33] = {0};



void setup()
{
  Serial.begin(9600);
  BigNumber::begin();

  delay(500);
  publickey = PublicKeyGen();
  privatekey = PrivateKeyGen(); //could be done at the very beginning, before serial.begin, so the calculations are done very early.
  Serial.print("PublicKey: ");
  Serial.println(publickey);

  Serial.print("PrivateKey: ");
  Serial.println(privatekey);

  
  delay(500);
  
  BTSerial.begin(38400);  // HC-05 default speed in AT command more
  Serial.println("Bluetooth Serial runnning correctly on MASTER");
} // End of Setup.

void loop(){
  if (state == 0){
    delay(2500);
    Serial.println("State: 0");
    myString = readBluetooth();
    if (myString == "Request RSAKey"){
      Serial.print("Received: ");
      Serial.println(myString);
      state = 1;
    }
  }
  if (state == 1){
    delay(2500);
    Serial.println();
    Serial.println("State: 1");

    BTSerial.flush();
    sendBigNumber(publickey);
    Serial.print("Sending: ");
    Serial.println("RSA PublicKey");
    
    state = 2;
  }
  if (state == 2){
    delay(2500);
    Serial.println();
    Serial.println("State: 2");
    
    myString = readBluetooth();
    Serial.print("Received encrypted AES_KEY: ");
    Serial.println(myString);
    BigNumber ENC_AESKey = castToBignumber(myString);
    AesKey = Decrypt(ENC_AESKey, publickey, privatekey);
    fromBignumberToIntarray(AesKey,AES_key);
    Serial.print("Decrypted AES_Key: ");
    Serial.println(AesKey);
    
    
    state = 3;
  }
  if (state == 3){
    delay(2500);
    Serial.println();
    Serial.println("State: 3");
    sendStringNumber("AES Key received...");
    Serial.println("Sending: AES Key received...");
    Serial.println();
    state = 4;
    AesComm = true;
  }

  Serial.print("AES communication enabled: ");
  if (AesComm){
    Serial.println("TRUE");
  } else {
    Serial.println("FALSE");
  }
      
  if (AesComm){
    // Read encrypted message
    encAesMsg = readBluetooth();
    fromStringToIntarray(encAesMsg,holderAes);
    printIntArray("Encrypted message: ",holderAes,16);

    // Print decrypted message
    decryption(holderAes, AES_key);
    printIntArray("Decrypted message: ",holderAes,16);

    // Print decrypted message ascii
    Serial.print("Decrypted message Text: ");
    intArrayToString(holderAes);
    Serial.println();

    delay(3000);
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



BigNumber castToBignumber(String msg){
  char temp[(msg.length()+1)];
  msg.toCharArray(temp, (msg.length()+1));
  return temp;
} // End of castToBignumber.



void hexToCharAESArray(char *src){
  int place = 0;
  for (int i=0; i<16; i++)
    place += sprintf(&src[place], "%d", AES_key[i]); //this is magic man. 
} // End of hexToCharAESArray.



void fromStringToIntarray(String src, int *dst){
  char HoldRes;
  for (int i = 0; i < 16; i++){
    HoldRes = src[i];
    dst[i] = (int) HoldRes;
  }
} // End of fromStringToIntarray



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
} // End of intArrayToString. 


void fromBignumberToIntarray(BigNumber src, int *dst){
  String tempKeyHolder = src.toString();
  String HoldRes;
  for (int i = 0; i < 16; i++){
    HoldRes = "";
    HoldRes += tempKeyHolder[(i*2)];
    HoldRes += tempKeyHolder[((i*2)+1)];
    
    dst[i] = HoldRes.toInt();
  }
} // End of fromBignumberToIntarray.

void printIntArray(String prefix, int *src, int sizeArray){
  delay(50);
  Serial.print(prefix);
  for (int i = 0; i < sizeArray; i++){
      Serial.print(src[i]);
      Serial.print(" ");
    }
    Serial.println();
}

