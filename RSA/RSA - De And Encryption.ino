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


/////////// Fully Setup ///////////////////


void setup ()
{
  Serial.begin (115200);


  
  BigNumber::begin ();

  /////////// SIMPLE KEY GENERATION EXMAPLE ///////////////////
  
  /////////// Primes ///////////
  BigNumber p = "54067457335566690463491306271848765326184947240747140586030469016394769687754285335901116176869704797123875321935451612607953265643676637953263307515077267";
  BigNumber q = "13987224189657867166936253773878341379794529237492529974312848742885908945282101763937324820487180200413163362055032121172865635463986138886748450771845601";
  //BigNumber p = "37975227936943673922808872755445627854565536638199";
  //BigNumber q = "40094690950920881030683735292761468389214899724061";
  //BigNumber p = "15397914917960409350788738354304881";
  //BigNumber q = "17914286717512723914819353467130831";


  /////////// Key ///////////
  BigNumber n = p*q; //RSA 1024
  Serial.print("The public key (n) is equal to : ");Serial.println(n);

  /////////// Relative Prime ///////////
  BigNumber e = "823";

  /////////// Phi ///////////
  BigNumber phi = (p-"1")*(q-"1"); //øhhh, det virkede ikke lige med normal et'ere men burde virke nu 
  Serial.print("The phi function is equal to   : ");Serial.println(phi);

  /////////// Modular Inverse ///////////
  BigNumber d = modInv(e,phi);
  Serial.print("The modular inverse is equal to: ");
  Serial.println(d);

  //////////////// SIMPLE ENCRYPTION EXAMPLE ////////////////////
  BigNumber m = "84726584832077892075797871207085"; 
  //BigNumber m = "72"; //what we want to send! which is 'H' in ascii
  BigNumber me = m.powMod (e,n); //test which method is fastest.
  Serial.print ("The cipher text is equal to:  ");
  Serial.println(me);

  Serial.println("");
  Serial.println("Finished encryption, ready to transfer");

  /*
  
  //////////////// SIMPLE DECRYPTION EXAMPLE ////////////////////

  unsigned long start = millis();
  
  BigNumber cd = me.powMod(d,n);
  
  unsigned long endx = millis();
  unsigned long elapsed = endx -start;
  
  Serial.println();
  
  Serial.print("Milisecond elapsed: ");Serial.println(elapsed);

  Serial.println();
  
  
  Serial.print("The receiver has received: ");
  Serial.println(cd);
  
  */
  
  
}

void loop () { }
