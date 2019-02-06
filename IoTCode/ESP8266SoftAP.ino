//////////////////// IMPORTS /////////////////////////////
#include <ESP8266WiFi.h>
#include <elapsedMillis.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
elapsedMillis timeElapsed;

//note
// we should probably be using wifi.STATIONAP
// combination of wifi.STATION and wifi.SOFTAP. It allows you to create a local WiFi connection and connect to another WiFi router.
//////////////////// GLOBALS /////////////////////////////

const int interval = 5000;
const char ssidsoft[] = "dank"; //max 31 characters
const char pass_soft[]= "ledank1234"; //least 8 characters, max 63, configured with WPA2-PSK
const int chnl = 4; //channel of WiFi (1 to 13)
const int ssidsoft_hidden = 0; //0 = false, not hidden    1 = true, wifi is then hidden
const int maxconnections = 8; // max simultaneous connected station, 0 to 8

bool softapcheck;
bool stringComplete = false;  // whether the string is complete

const char ssidSTA[] = "Wifitest"; //ssid and password for the wifi we're connecting to in STA mode. 
const char passSTA[]= "pingpongok5"; 

uint8_t macAddr[6]; //placeholder for macAddr of Soft-AP (uint8_t is unsigned integeers of 8 bits)


String inputString = "";         // a String to hold incoming data

////PROTO TYPE DECLARATIONS ///
void serialEvent(void); //return type is void, input is void, hence the declaration.
void softAPmode(void);
void STATAPmode(void);


//////////////////// SETUP CALL /////////////////////////////
void setup() {
  Serial.begin(115200); //Serial fastest baud rate possible.
  // reserve 200 bytes for the inputString:
  inputString.reserve(200);

  while(stringComplete == false){
    serialEvent(); //måske skal den her fjernes siden den heletiden tjekker serial nede i selve funktionen uden rent faktisk at blive kaldt.
    
  }
  Serial.println("The AP mode was entered: ");
  Serial.println(inputString);

  if(inputString == "SOFTAP"){
    //run softAP setup
    softAPmode();
  }
  else if (inputString == "STATAP"){
    STATAPmode();
    
  }
  else if (inputString == "SOFTSTAT"){
    //Run Soft+STAT mode
  }
  else{ //print errror code and run standard softAP
    Serial.println("NO VALID AP MODE ENTERED, DEFAULTING TO SOFT AP.");
    softAPmode();
  }

  


  
}

void loop() {
  if(timeElapsed >= interval){
    Serial.printf("Stations connected to soft-AP = %d\n", WiFi.softAPgetStationNum());
    timeElapsed = 0;
  }
   
  }


void softAPmode(){
  
  Serial.print("Setting up initial soft-AP Mode  ... ");
  WiFi.mode(WIFI_AP);
  softapcheck = WiFi.softAP(ssidsoft, pass_soft, chnl, ssidsoft_hidden, maxconnections); //softAP function returns true/false depending on result of the setup
  if(softapcheck == true){
    Serial.println("WiFi SoftAP mode has been succesfully set up, with the following settings:");
    Serial.println("SSID: ");
    Serial.print(ssidsoft);
    Serial.println("Password: ");
    Serial.println(pass_soft);
    Serial.println("Channel: ");
    Serial.print(chnl);
    Serial.println("The WiFi is ");
    if(ssidsoft_hidden == 0){
      Serial.print("NOT hidden");
    }
    else{
      Serial.print("HIDDEN");
    }
    
    Serial.println("Able to handle # connections: ");
    Serial.print(maxconnections);

    Serial.print("Soft-AP IP address = ");
    Serial.print(WiFi.softAPIP());
    WiFi.softAPmacAddress(macAddr);
    Serial.println();
    Serial.printf("MAC address = %02x:%02x:%02x:%02x:%02x:%02x\n", macAddr[0], macAddr[1], macAddr[2], macAddr[3], macAddr[4], macAddr[5]);
    
  }
  else{
    Serial.println("ERROR: Could not set up SoftAP Mode for ESP8266 NodeMCU");
  }
}

void STATAPmode(){

  //we let the DHCP server assign us an IP, and set up the configurations, these could be manually defined as seen here:
  //xx
  
  WiFi.begin(ssidSTA,passSTA); //CONNECTING TO WIFI
  while (WiFi.status() != WL_CONNECTED) { //testing if we can actually connect to the specified wifi
    delay(500);
    Serial.print(".");
  }
  Serial.println();
  Serial.print("Connected to SSID: ");
  Serial.println(ssidSTA);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());  //Print the assigned IP 
  
}

void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the inputString:
    inputString += inChar;
    // if the incoming character is a newline, set a flag so the main loop can
    // do something about it:
    if (inChar == '\n') {
      stringComplete = true;
    }
  }
}


  
