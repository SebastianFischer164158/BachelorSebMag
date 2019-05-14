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
  Serial.begin (9600);
  BigNumber::begin ();
  
  BigNumber p = "9932139943339554751655031442828579353277196020045387852012083330216751";
  BigNumber q = "7104411554778760027250011387254928276716637756917863968861551676876553";

  unsigned long start = millis();
  BigNumber n = p*q; //RSA 1024
  BigNumber e = "307";
  BigNumber phi = (p-"1")*(q-"1");
  BigNumber d = modInv(e,phi);
  unsigned long endx = millis();
  unsigned long elapsed = endx -start;
  delay(100);
  Serial.print("Milisecond elapsed Keygen: ");Serial.println(elapsed);
  
  BigNumber m = "84726584832077892075797871207085"; 
  
  start = millis();
  BigNumber me = m.powMod (e,n); //test which method is fastest.
  endx = millis();
  elapsed = endx - start;
  delay(100);
  Serial.print("Milisecond elapsed Encryption: ");Serial.println(elapsed);


  start = millis();
  ESP.wdtDisable(); // Thise disable WatchDogTimer, makes the arduino able to calculate large integers. Det virker i hvert fald
  BigNumber cd = me.powMod(d,n);
  endx = millis();
  elapsed = endx -start;
  delay(100);
  Serial.print("Milisecond elapsed Decryption: ");Serial.println(elapsed);
  Serial.println(cd);
}

void loop() {
  // put your main code here, to run repeatedly:

}
