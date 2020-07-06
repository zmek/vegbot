/*

 This connects to the remote database and writes data from the MKR ENV shield
 */
#include <SPI.h>
#include <WiFiNINA.h>
#include <Arduino_MKRENV.h>


#include "arduino_secrets.h" ser
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

void setup() {

  // check for the WiFi module:
  if (WiFi.status() == WL_NO_MODULE) {
    // don't continue
    while (true);
  }

//  String fv = WiFi.firmwareVersion();
//  if (fv < WIFI_FIRMWARE_LATEST_VERSION) {
//    Serial.println("Please upgrade the firmware");
//  }

  // attempt to connect to Wifi network:
  while (status != WL_CONNECTED) {
    Serial.print("Attempting to connect to WPA SSID: ");
    Serial.println(ssid);
    // Connect to WPA/WPA2 network:
    status = WiFi.begin(ssid, pass);

    // wait 10 seconds for connection:
    delay(10000);
  }

//  // you're connected now, so print out the data:
  Serial.print("You're connected to the network");
  printCurrentNet();
  printWifiData();

  // check the env shield:
  if (!ENV.begin()) {
    Serial.println("Failed to initialize MKR ENV shield!");
    while (1);
  }

}

void loop() {

  // if there are incoming bytes available
  // from the server, read them and print them:
  while (client.available()) {
    char c = client.read();
    Serial.write(c);
  }


   // read all the sensor values
  float temperature = ENV.readTemperature();
  float humidity    = ENV.readHumidity();
  float pressure    = ENV.readPressure();
  float illuminance = ENV.readIlluminance();
  float uva         = ENV.readUVA();
  float uvb         = ENV.readUVB();
  float uvIndex     = ENV.readUVIndex();

  // read wifi signal
  long rssi = WiFi.RSSI();

  // check wifi connection
  if (rssi == 0) {  //no connection
        while (status != WL_CONNECTED) {
          status = WiFi.begin(ssid, pass);
    
          // wait 10 seconds for connection:
          delay(10000);
      }
    }

  // send to php
  sendToPHP(temperature, humidity, pressure, illuminance, uva, uvb, uvIndex, rssi);

  Serial.println("Finished sending");

  // wait 10 minutes:
  delay(10000);
//  printCurrentNet();
}

void printWifiData() {
  // print your board's IP address:
  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);
  Serial.println(ip);

  // print your MAC address:
  byte mac[6];
  WiFi.macAddress(mac);
  Serial.print("MAC address: ");
  printMacAddress(mac);
}

void printCurrentNet() {
  // print the SSID of the network you're attached to:
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());

  // print the MAC address of the router you're attached to:
  byte bssid[6];
  WiFi.BSSID(bssid);
  Serial.print("BSSID: ");
  printMacAddress(bssid);

  // print the received signal strength:
  long rssi = WiFi.RSSI();
  Serial.print("signal strength (RSSI):");
  Serial.println(rssi);

  // print the encryption type:
  byte encryption = WiFi.encryptionType();
  Serial.print("Encryption Type:");
  Serial.println(encryption, HEX);
  Serial.println();
}

void printMacAddress(byte mac[]) {
  for (int i = 5; i >= 0; i--) {
    if (mac[i] < 16) {
      Serial.print("0");
    }
    Serial.print(mac[i], HEX);
    if (i > 0) {
      Serial.print(":");
    }
  }
  Serial.println();
}

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
   if (client.connect(server, 80)) {
    Serial.print("Made a connection to the server");
     // Make a HTTP request:
    Serial.print("POST /api/writedata.php HTTP/1.1");
    client.print("POST /api/writedata.php HTTP/1.1");     
    client.println();
    Serial.println();
    client.println("Host: vegbot.io");
    Serial.println("Host: vegbot.io");

    client.print("loc=");
    Serial.println("loc=");
    Serial.println(2);
    client.print(2);
    
    client.print("&temp=");
    Serial.println("&temp=");
    client.print(temperature);
    Serial.println(temperature);
    
    client.print("&humidity=");
    Serial.println("&humidity=");
    Serial.println(humidity);
    client.print(humidity);

    client.print("&pressure=");
    Serial.println("&pressure=");
    Serial.println(pressure);
    client.print(pressure);

    client.print("&illuminance=");
    Serial.println("&illuminance=");
    Serial.println(illuminance);
    client.print(illuminance);

    client.print("&uva=");
    Serial.println("&uva=");
    Serial.println(uva);
    client.print(uva);

    client.print("&uvb=");
    Serial.println("&uvb=");
    Serial.println(uvb);
    client.print(uvb);

    client.print("&uvindex=");
    Serial.println("&uvindex=");
    Serial.println(uvIndex);
    client.print(uvIndex);

    client.print("&rssi=");
    Serial.println("&rssi=");
    Serial.println(rssi);
    client.print(rssi);
    
    client.println();
    Serial.println();
    client.println("Connection: close");
    Serial.println("Connection: close");



  } else {
    // if you didn't get a connection to the server:
    Serial.println("connection failed");
  }
 }
