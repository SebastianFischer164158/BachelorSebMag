#include <SoftwareSerial.h>
#include "AES.h"
char array1[16] = {0};
char result[16] = {0};
int decryptarray[16] = {0};
SoftwareSerial BTSerial(D6, D7); // RX | TX
int key[16] = {0x54, 0x68, 0x61, 0x74, 0x73, 0x20, 0x6d, 0x79, 0x20, 0x4b, 0x75, 0x6e, 0x67, 0x20, 0x46, 0x75};
int counter = 0;
void setup()
{ 
  Serial.begin(9600);

  int plaintext[16] = {0}; 
  BTSerial.begin(38400);  // HC-05 default speed in AT command more
}
 
void loop(){
  // Keep reading from HC-05 and send to Arduino Serial Monitor
  if (BTSerial.available())
  {
    
    if(counter<16){
      array1[counter] = BTSerial.read();
      counter++;
    }
    if(counter>=16){
      charToInt(array1,decryptarray);
      decryption(decryptarray,key);
      printArrayHex(decryptarray,16);
      intToChar(decryptarray,result);
      printArray(result,16);
      counter = 0; 
    }
    
    //Serial.write(BTSerial.read()); til AT mode
    
  }
  
  
  
    

  // Keep reading from Arduino Serial Monitor and send to HC-05
  if (Serial.available())
    BTSerial.write(Serial.read());
}
