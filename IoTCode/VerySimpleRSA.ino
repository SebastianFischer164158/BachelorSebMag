// the setup function runs once when you press reset or power the board
#include <math.h>

int modInverse(int a, int m) 
{ 
    a = a%m; 
    for (int x=1; x<m; x++) 
       if ((a*x) % m == 1) 
          return x; 
} 
void setup() {
  Serial.begin(115200);
  int p = 11;
  int q = 17;
  int e = 3;

  int n = p*q;

  int phi = (p-1)*(q-1);
  int d = modInverse(e,phi);
  Serial.println("The modular inverse is equal to : ");Serial.print(d);


  //we now send 'H' which is 72 in ASCII so m = 72
  //we then calculate
  int m = 72;
  int me = (int)(pow(m,e))% n;
  Serial.println("The me is equal to : ");Serial.print(me);


  int cd = (int)(pow(
  


  


  
}

// the loop function runs over and over again forever
void loop() {
  digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
  delay(1000);                       // wait for a second
  digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
  delay(1000);                       // wait for a second
}
