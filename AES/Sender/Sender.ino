#include <SoftwareSerial.h>
#include "AES.h"

SoftwareSerial BTSerial(D6, D7); // RX | TX
int key[16] = {0x54, 0x68, 0x61, 0x74, 0x73, 0x20, 0x6d, 0x79, 0x20, 0x4b, 0x75, 0x6e, 0x67, 0x20, 0x46, 0x75};
int plaintext[16] = {0};
char intputSerial[16] = {0};
void setup()
{ 
  pinMode(D5,OUTPUT);
  digitalWrite(D5,HIGH);
  Serial.begin(9600);
  delay(500);

  char input[16] = {'T','H','A','T'};
  char output[16];
  
  charToInt(input,plaintext);

  printArrayHex(plaintext,16);
  
  delay(500);
  encryption(plaintext,key);
  delay(500);

  printArrayHex(plaintext,16);
  
  Serial.println("Enter AT commands:");
  BTSerial.begin(38400);  // HC-05 default speed in AT command more

  delay(500);
  for (int i = 0; i < 16; i++){
    BTSerial.write(plaintext[i]);
  }
  
  
}

void loop(){
  // Keep reading from HC-05 and send to Arduino Serial Monitor
  if (BTSerial.available())
    Serial.write(BTSerial.read());

  // Keep reading from Arduino Serial Monitor and send to HC-05
  if (Serial.available()){
    BTSerial.write(Serial.read());
  }
}
