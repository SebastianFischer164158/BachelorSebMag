#include <BigNumber.h>

BigNumber x = 0;
BigNumber y = 0;

void extendedEuclid(BigNumber InputNumbOne, BigNumber InputNumbTwo)
{
  BigNumber temp;                      
  if(InputNumbTwo == "0")
  {
      x = "1";
      y = "0";
  }
  else
  {
      extendedEuclid(InputNumbTwo,InputNumbOne % InputNumbTwo);
      temp = x;
      x = y;
      y = temp - (InputNumbOne / InputNumbTwo) * y;
  }
}

BigNumber modInv(BigNumber MI_One, BigNumber MI_Two)
{
    extendedEuclid(MI_One, MI_Two);
    // X is the coefficient.
    if (x < "0"){
      x += MI_Two;
    }
        
    return x;
}

void setup() {
  Serial.begin(9600);
  BigNumber::begin();
  
  BigNumber p = "";
  BigNumber q = "";

  unsigned long start_generation = millis();
  BigNumber n = p*q;  // public key
  BigNumber e = "307";
  BigNumber phi = (p-"1")*(q-"1");
  BigNumber d = modInv(e,phi); // private key
  unsigned long end_generation = millis();
  unsigned long elapsed_generation = end_generation - start_generation;
  delay(100);
  Serial.print("Milisecond elapsed Keygen: ");
  Serial.println(elapsed_generation);
  
  BigNumber m = "84726584833277893275857871327085";
  //THATS MY KUNG FU
  //84 72 65 84 83 32 77 89 32 75 85 78 71 32 70 85      (this is in decimal bytes) 
  //https://www.rapidtables.com/convert/number/ascii-hex-bin-dec-converter.html
  
  start_encrypt = millis();
  BigNumber me = m.powMod(e,n); //encryption is done on the whole message. 
  end_encrypt = millis();
  elapsed_encrypt = end_encrypt - start_encrypt;
  delay(100);
  Serial.print("Milisecond elapsed Encryption: ");
  Serial.println(elapsed_encrypt);


  start_decrypt = millis();
  BigNumber cd = me.powMod(d,n);
  end_decrypt = millis();
  elapsed_decrypt = end_decrypt - start_decrypt;
  delay(100);
  Serial.print("Milisecond elapsed Decryption: ");
  Serial.println(elapsed_decrypt);
  Serial.println(cd);
}

void loop() {
  // put your main code here, to run repeatedly:

}
