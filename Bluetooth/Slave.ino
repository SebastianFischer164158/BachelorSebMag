#include <SoftwareSerial.h>
#include "AES.h"
#include "RSA.h"

SoftwareSerial BTSerial(D6, D7); // RX | TX
int state = 0;

String msg = "Request RSAKey";
bool hi = true;


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
  }
}

void sendStringNumber(String msg){
  for (int i = 0; i < msg.length(); i++){
    BTSerial.write(msg[i]);
  }
}



void setup()
{
  Serial.begin(9600);
  BigNumber::begin();
  
  delay(500);
  
  BTSerial.begin(38400);  // HC-05 default speed in AT command more
  Serial.println("Bluetooth Serial runnning correctly on SLAVE");
}

String temper;
void loop(){
  if (state == 0){
    Serial.println("State: 0");
    
    // Sending char array
    sendStringNumber(msg);
    BTSerial.flush();
    Serial.print("Sending: ");
    Serial.println("RSA Request");
    
    state = 1;
  }
  if (state == 1){
    delay(200);
    Serial.println("State: 1");
    
    String tempMe = readBluetooth();
    BTSerial.flush();
    Serial.print("Received: ");
    Serial.println(tempMe);
    
    state = 2;
  }
  if (state == 2){
    delay(200);
    Serial.println("State: 2");

    temper = readBluetooth();
    BTSerial.flush();
    Serial.print("Received test: ");
    Serial.println(temper);
    
    state = 3;
  }
  if (state == 3){
    Serial.println("State: 3");

    state = 4;
  }


delay(1000);
}
