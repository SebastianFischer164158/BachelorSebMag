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

void fromBignumberToIntarray(BigNumber src, int *dst){
  //String tempKeyHolder = src.toString();
  String tempKeyHolder = src.toString();
  String HoldRes;
  
  for (int i = 0; i < 16; i++){
    HoldRes = "";
    HoldRes += tempKeyHolder[(i*2)];
    HoldRes += tempKeyHolder[((i*2)+1)];
    
    dst[i] = HoldRes.toInt();
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

BigNumber RSA_encryption(BigNumber msg, BigNumber PublicKey)
{
  BigNumber CoPrime= 307;
  BigNumber encryption = msg.powMod(CoPrime,PublicKey);
  return encryption;
}

BigNumber RSA_decryption(BigNumber EncryptedMsg, BigNumber PublicKey, BigNumber PrivateKey)
{
  BigNumber decryption = EncryptedMsg.powMod(PrivateKey,PublicKey);
  return decryption;
}

BigNumber PublicKeyGen()
{
  BigNumber firstPrime = "34169090529181804975509056946439162865195316898547061713223274034873259174398131810568013649207194042897653590213438750899278631021362723640271358164566011";
  BigNumber secondPrime = "6480748263904619031680260331936564669623869952492469641161930262856628003360317687993928982065215349138700631936521201127616864444987232349342262924810817";
  BigNumber PublicKey = firstPrime * secondPrime;
  return PublicKey;
}

BigNumber PrivateKeyGen()
{
  BigNumber firstPrime = "34169090529181804975509056946439162865195316898547061713223274034873259174398131810568013649207194042897653590213438750899278631021362723640271358164566011";
  BigNumber secondPrime = "6480748263904619031680260331936564669623869952492469641161930262856628003360317687993928982065215349138700631936521201127616864444987232349342262924810817";
  BigNumber CoPrime = "307";
  BigNumber phi = (firstPrime-"1") * (secondPrime-"1");
  BigNumber PrivateKey = modInv(CoPrime,phi);
  return PrivateKey;
}
