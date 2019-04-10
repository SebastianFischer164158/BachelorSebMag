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
  BigNumber CoPrime = 307;
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
  //BigNumber firstPrime = "15397914917960409350788738354304881";
  //BigNumber secondPrime = "17914286717512723914819353467130831";
  //rsa 512
  //BigNumber firstPrime = "73876994494307542360607835849776308028761548518813298873221350532322237104687";
  //BigNumber secondPrime = "321538625144835508338276064648892293814103155617777116608040141481480882702241";
  //rsa 1024
  BigNumber firstPrime = "34169090529181804975509056946439162865195316898547061713223274034873259174398131810568013649207194042897653590213438750899278631021362723640271358164566011";
  BigNumber secondPrime = "6480748263904619031680260331936564669623869952492469641161930262856628003360317687993928982065215349138700631936521201127616864444987232349342262924810817";
  BigNumber PublicKey = firstPrime * secondPrime;
  return PublicKey;
}

BigNumber PrivateKeyGen()
{
  //BigNumber firstPrime = "15397914917960409350788738354304881";
  //BigNumber secondPrime = "17914286717512723914819353467130831";
  //rsa 512
  //BigNumber firstPrime = "73876994494307542360607835849776308028761548518813298873221350532322237104687";
  //BigNumber secondPrime = "321538625144835508338276064648892293814103155617777116608040141481480882702241";
  //rsa 1024
  BigNumber firstPrime = "34169090529181804975509056946439162865195316898547061713223274034873259174398131810568013649207194042897653590213438750899278631021362723640271358164566011";
  BigNumber secondPrime = "6480748263904619031680260331936564669623869952492469641161930262856628003360317687993928982065215349138700631936521201127616864444987232349342262924810817";
  BigNumber CoPrime = "307";
  BigNumber phi = (firstPrime-"1") * (secondPrime-"1");
  BigNumber PrivateKey = modInv(CoPrime,phi);
  return PrivateKey;
}
