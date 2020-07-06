/*

 This connects to the remote database and writes data from the MKR ENV shield
 */
#include <SPI.h>
#include <WiFiNINA.h>
#include <Arduino_MKRENV.h>
#include <SD.h>

// chip select for SD card
const int SD_CS_PIN = 4;

// set arduino ID
const int loc = 2;

#include "arduino_secrets.h" 
///////please enter your sensitive data in the Secret tab/arduino_secrets.h
char ssid[] = SECRET_SSID;        // your network SSID (name)
char pass[] = SECRET_PASS;    // your network password (use for WPA, or use as key for WEP)
int status = WL_IDLE_STATUS;     // the Wifi radio's status

char server[] = "vegbot.io";
//IPAddress server(31,170,123,74);

// Initialize the Ethernet client library
// with the IP address and port of the server
// that you want to connect to (port 80 is default for HTTP):
WiFiClient client;

// file object
File dataFile;

void setup() {

  // check the env shield:
  if (!ENV.begin()) {
//    Serial.println("Failed to initialize MKR ENV shield!");
    while (1);
  }

  // init the logfile
  dataFile = SD.open("log-0000.csv", FILE_WRITE);
  delay(1000);

    // init the CSV file with headers
  dataFile.println("loc,temp,humidity,pressure,uva,uvb,uvIndex");

  // close the file
  dataFile.close();
  delay(100);
  
  // check for the WiFi module:
  if (WiFi.status() == WL_NO_MODULE) {
    // don't continue
    while (true);
  }

  String fv = WiFi.firmwareVersion();
  if (fv < WIFI_FIRMWARE_LATEST_VERSION) {
    dataFile.println("Please upgrade the firmware");
  }

  // attempt to connect to Wifi network:
  while (status != WL_CONNECTED) {
//    Serial.print("Attempting to connect to WPA SSID: ");
//    Serial.println(ssid);
    // Connect to WPA/WPA2 network:
    status = WiFi.begin(ssid, pass);

    // wait 10 seconds for connection:
    delay(10000);
  }

//  // you're connected now, so print out the data:
//  Serial.print("You're connected to the network");
//  printCurrentNet();
//  printWifiData();


}

void loop() {

  // init the logfile
  dataFile = SD.open("log-0000.csv", FILE_WRITE);
  delay(1000);

   // read all the sensor values
  float temperature = ENV.readTemperature();
  float humidity    = ENV.readHumidity();
  float pressure    = ENV.readPressure();
  float illuminance = ENV.readIlluminance();
  float uva         = ENV.readUVA();
  float uvb         = ENV.readUVB();
  float uvIndex     = ENV.readUVIndex();

  // print each of the sensor values
  dataFile.print(loc);
  dataFile.print(",");  
  dataFile.print(temperature);
  dataFile.print(",");
  dataFile.print(humidity);
  dataFile.print(",");
  dataFile.print(pressure);
  dataFile.print(",");
  dataFile.print(uva);
  dataFile.print(",");
  dataFile.print(uvb);
  dataFile.print(",");
  dataFile.println(uvIndex);  //note - println used for the last one

  // close the file
  dataFile.close();

  // check wifi connection
  if (rssi == 0) {  //no connection
        while (status != WL_CONNECTED) {
          status = WiFi.begin(ssid, pass);
    
          // wait 10 seconds for connection:
          delay(10000);
      }
    }

  // send to php
  sendToPHP(loc, temperature, humidity, pressure, illuminance, uva, uvb, uvIndex, rssi);
  


  // wait 1 minutes:
  delay(60000);
//  printCurrentNet();
}

//void printWifiData() {
//  // print your board's IP address:
//  IPAddress ip = WiFi.localIP();
//  Serial.print("IP Address: ");
//  Serial.println(ip);
//  Serial.println(ip);
//
//  // print your MAC address:
//  byte mac[6];
//  WiFi.macAddress(mac);
//  Serial.print("MAC address: ");
//  printMacAddress(mac);
//}
//
//void printCurrentNet() {
//  // print the SSID of the network you're attached to:
//  Serial.print("SSID: ");
//  Serial.println(WiFi.SSID());
//
//  // print the MAC address of the router you're attached to:
//  byte bssid[6];
//  WiFi.BSSID(bssid);
//  Serial.print("BSSID: ");
//  printMacAddress(bssid);
//
//  // print the received signal strength:
//  long rssi = WiFi.RSSI();
//  Serial.print("signal strength (RSSI):");
//  Serial.println(rssi);
//
//  // print the encryption type:
//  byte encryption = WiFi.encryptionType();
//  Serial.print("Encryption Type:");
//  Serial.println(encryption, HEX);
//  Serial.println();
//}
//
//void printMacAddress(byte mac[]) {
//  for (int i = 5; i >= 0; i--) {
//    if (mac[i] < 16) {
//      Serial.print("0");
//    }
//    Serial.print(mac[i], HEX);
//    if (i > 0) {
//      Serial.print(":");
//    }
//  }
//  Serial.println();
//}

//CONNECTING WITH MYSQL
void sendToPHP( 
  float temperature, 
  float humidity,
  float pressure,
  float illuminance,
  float uva,
  float uvb,
  float uvIndex,
  long rssi)   
 {
   if (client.connectSSL(server, 443)) {
    // Make a HTTP request:
    client.print("GET /api/writedata.php?loc=");     //YOUR URL
    client.print(loc);
    
    client.print("&temp=");
    client.print(temperature);
    
    client.print("&humidity=");
    client.print(humidity);

    client.print("&pressure=");
    client.print(pressure);

    client.print("&illuminance=");
    client.print(illuminance);

    client.print("&uva=");
    client.print(uva);

    client.print("&uvb=");
    client.print(uvb);

    client.print("&uvindex=");
    client.print(uvIndex);

    client.print("&rssi=");
    client.print(rssi);
    
    client.print(" ");      //SPACE BEFORE HTTP/1.1
    client.print("HTTP/1.1");
    client.println();
    client.println("Host: vegbot.io");
    client.println("Connection: close");
    client.println();
  }
 }
 
