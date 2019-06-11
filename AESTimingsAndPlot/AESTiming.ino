#include "AES.h"

unsigned long timeencryptarray[250] = {0};
unsigned long timedecryptarray[250] = {0};
char testdata[] = "Two One Nine Two";
int key[16] = {0x54, 0x68, 0x61, 0x74, 0x73, 0x20, 0x6d, 0x79, 0x20, 0x4b, 0x75, 0x6e, 0x67, 0x20, 0x46, 0x75};

unsigned long start_encrypt = 0;
unsigned long end_encrypt = 0;
unsigned long start_decrypt = 0;
unsigned long end_decrypt = 0;
unsigned long elapsed_encrypt = 0;
unsigned long elapsed_decrypt = 0;
char output[16] = {0};

void setup() {
  
  Serial.begin(115200);
  int plaintext[16] = {0};
  charToInt(testdata,plaintext);
  
  Serial.println("Testdata is: ");
  Serial.println(testdata);
  Serial.println();
  delay(1000);
  printArrayHex(plaintext,16);
  for(int i = 0; i<250;i++){
    output[16] = {0};
    start_encrypt = 0;
    end_encrypt = 0;
    start_decrypt = 0;
    end_decrypt = 0;
    elapsed_encrypt = 0;
    elapsed_decrypt = 0;
    start_encrypt = micros();
    AES_encryption(plaintext,key);
    end_encrypt = micros();
    elapsed_encrypt = end_encrypt - start_encrypt;
    timeencryptarray[i] = elapsed_encrypt;


    start_decrypt = micros();
    AES_decryption(plaintext,key);
    end_decrypt = micros();
    elapsed_decrypt = end_decrypt - start_decrypt;
    timedecryptarray[i] = elapsed_decrypt;


  }
  Serial.println("ENCRYPTION TIME: ");
  
  for(int o = 0; o < 250; o++) {
  Serial.print(timeencryptarray[o]);
  Serial.print(",");
}
  Serial.println();
  Serial.println("DECRYPTION TIME: ");
    for(int l = 0; l < 250; l++)
{
  Serial.print(timedecryptarray[l]);
  Serial.print(",");
}
}
void loop() {}
