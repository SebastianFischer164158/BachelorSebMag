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
  
  BigNumber p = "12131072439211271897323671531612440428472427633701410925634549312301964373042085619324197365322416866541017057361365214171711713797974299334871062829803541"; //prime 1
  BigNumber q = "12027524255478748885956220793734512128733387803682075433653899983955179850988797899869146900809131611153346817050832096022160146366346391812470987105415233"; //prime 2
  delay(1000);
  Serial.println();
  Serial.print("p prime: ");
  Serial.println(p);
  Serial.println();
  Serial.print("q prime: ");
  Serial.println(q);
  

  BigNumber n = p*q;  // public key
  BigNumber e = "65537";
  BigNumber phi = (p-"1")*(q-"1");
  BigNumber d = modInv(e,phi); // private key
  
  delay(1000);
  Serial.println();
  Serial.print("e: ");
  Serial.println(e);
  
  Serial.println();
  Serial.print("Phi: ");
  Serial.println(phi);
  
  Serial.println();
  Serial.print("PublicKey: ");
  Serial.println(phi);
  
  Serial.println();
  Serial.print("PrivateKey: ");
  Serial.println(n);
 
  delay(100);
  
  BigNumber m = "1976620216402300889624482718775150";
  Serial.println();
  Serial.print("Input data: ");
  Serial.println(m);
  
  BigNumber me = m.powMod(e,n); //encryption is done on the whole message.

  Serial.println();
  Serial.print("Encrypted data: ");
  Serial.println(me);
  delay(100);

  //ESP.wdtDisable(); //only used with the esp8266 in order to remove the software watch dog timer 
  BigNumber cd = me.powMod(d,n);
  delay(100);
  Serial.println();
  Serial.print("Decrypted data: ");
  Serial.println(cd);
}

void loop() {

}
