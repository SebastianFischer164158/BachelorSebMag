#include <BigNumber.h>

// x and y are the remainder and coefficient
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

BigNumber Encrypt(BigNumber msg, BigNumber PublicKey)
{
  BigNumber CoPrime= 307;
  BigNumber encryption = msg.powMod(CoPrime,PublicKey);
  return encryption;
}

BigNumber Decrypt(BigNumber EncryptedMsg, BigNumber PublicKey, BigNumber PrivateKey)
{
  BigNumber decryption = EncryptedMsg.powMod(PrivateKey,PublicKey);
  return decryption;
}

BigNumber PublicKeyGen()
{
  BigNumber firstPrime = "15397914917960409350788738354304881";
  BigNumber secondPrime = "17914286717512723914819353467130831";
  BigNumber PublicKey = firstPrime * secondPrime;
  return PublicKey;
}

BigNumber PrivateKeyGen()
{
  BigNumber firstPrime = "15397914917960409350788738354304881";
  BigNumber secondPrime = "17914286717512723914819353467130831";
  BigNumber CoPrime = "307";
  BigNumber phi = (firstPrime-"1") * (secondPrime-"1");
  BigNumber PrivateKey = modInv(CoPrime,phi);
  return PrivateKey;
}
