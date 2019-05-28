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
  
  BigNumber p = "3674536715570527491566690287951037996197991603398601357951572341262652015472682909962471289162144327078018196450074365270956902387303469672209560485876936760165768272002090529902157310049944651653308441240723607748241072648854430684942215002444075095862627810361032947335194198388687577904995548344232923851411"; //prime 1
  BigNumber q = "5406224208221339752933301983500843680830138463166783717316933133915723830783939937097919412327866786859146719438900713803830457061950705600998974477130305556868955524249888840266526670555376680583898320813018824397037181175035157806372871892164260602958028923592067350657548556866276172521142347890253282211883"; //prime 2
  Serial.println();
  Serial.print("p prime : ");
  Serial.println(p);
  Serial.print("q prime : ");
  Serial.println(q);

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
  
  unsigned long start_encrypt = millis();
  BigNumber me = m.powMod(e,n); //encryption is done on the whole message. 
  unsigned long end_encrypt = millis();
  unsigned long elapsed_encrypt = end_encrypt - start_encrypt;
  delay(100);
  Serial.print("Milisecond elapsed Encryption: ");
  Serial.println(elapsed_encrypt);


  unsigned long start_decrypt = millis();
  BigNumber cd = me.powMod(d,n);
  unsigned long end_decrypt = millis();
  unsigned long elapsed_decrypt = end_decrypt - start_decrypt;
  delay(100);
  Serial.print("Milisecond elapsed Decryption: ");
  Serial.println(elapsed_decrypt);
  Serial.println(cd);
}

void loop() {

}
