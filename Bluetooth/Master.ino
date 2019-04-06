#include <SoftwareSerial.h>
#include "AES.h"
#include "RSA.h"

SoftwareSerial BTSerial(D6, D7); // RX | TX
int state = 0;

String readBluetooth(){
  String temp = "";
  ESP.wdtDisable();
  while (temp == ""){
    while (BTSerial.available()) {
      delay(20);  //small delay to allow input buffer to fill
    
      char c = BTSerial.read();  //gets one byte from serial buffer
      if (c == ',') {
        break;
      }  //breaks out of capture loop to print readstring
      temp += c;
    } //makes the string readString
  }
  return temp;
}

void sendBigNumber(BigNumber msg){
  String MyString = msg.toString();
  Serial.print("Length of RSAKey: ");
  Serial.println(MyString.length());
  for (int i = 0; i < MyString.length(); i++){
    BTSerial.write(MyString[i]);
    Serial.print(MyString[i]);
  }
}

void sendStringNumber(String msg){
  for (int i = 0; i < msg.length(); i++){
    BTSerial.write(msg[i]);
  }
}

BigNumber publickey = 0;
BigNumber privatekey = 0;
void setup()
{
  Serial.begin(9600);
  BigNumber::begin();

  delay(100);
  publickey = PublicKeyGen();
  privatekey = PrivateKeyGen(); //could be done at the very beginning, before serial.begin, so the calculations are done very early.
  Serial.print("PublicKey: ");
  Serial.println(publickey);

  Serial.print("PrivateKey: ");
  Serial.println(privatekey);

  
  delay(500);
  
  BTSerial.begin(38400);  // HC-05 default speed in AT command more
  Serial.println("Bluetooth Serial runnning correctly on MASTER");
}

String tester = "zxcvbnmasdfghjzxcvbnmzxcvbnmzxcvbnmzxcvbnmzxcvbnmzxcvbnmzxcvbnmzxcvbnmzxcvbnm";
char RSAKey[33] = {0};
String myString;
bool runable = true;
bool hi = true;

void loop(){
  if (state == 0){
    Serial.println("State: 0");
    myString = readBluetooth();
    BTSerial.flush();
    Serial.print("Received: ");
    Serial.println(myString);
    
    state = 1;
  }
  if (state == 1){
    delay(1000);
    Serial.println("State: 1");

    sendBigNumber(publickey);
    BTSerial.flush();
    Serial.print("Sending: ");
    Serial.println("RSA PublicKey");
    
    state = 2;
  }
  if (state == 2){
    delay(1000);
    Serial.println("State: 2");
     

    sendStringNumber(tester);
    BTSerial.flush();
    Serial.println("Test has been sent");
    

    state = 3;
  }
  if (state == 3){

    //state = 4;
  }


delay(1000);
}
