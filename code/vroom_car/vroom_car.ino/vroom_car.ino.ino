
#include <SPI.h>
#include <WiFi101.h>
#include <WiFiUdp.h>

#include <OSCBundle.h>
#include <OSCBoards.h>

#include <Servo.h>
#include <Wire.h>
#include <Adafruit_MotorShield.h>

int status = WL_IDLE_STATUS;
#include "arduino_secrets.h" 
///////please enter your sensitive data in the Secret tab/arduino_secrets.h
char ssid[] = SECRET_SSID;        // your network SSID (name)
char pass[] = SECRET_PASS;    // your network password (use for WPA, or use as key for WEP)
int keyIndex = 0;            // your network key Index number (needed only for WEP)

unsigned int localPort = 2390;      // local port to listen for UDP packets

// A UDP instance to let us send and receive packets over UDP
WiFiUDP Udp;

Servo servo;
int servoPos = 90;

Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 
Adafruit_DCMotor *motor = AFMS.getMotor(1);
int motorSpeed = 0;

void setup()
{
  // Open serial communications and wait for port to open:
  Serial.begin(9600);
  //while (!Serial) {
  //  ; // wait for serial port to connect. Needed for native USB port only
  //}

  connectToWifi();

  // servo setup
  servo.attach(A4);

  // dc motor setup
  AFMS.begin();
  motor->setSpeed(0);
  motor->run(FORWARD);
  // turn on motor
  motor->run(RELEASE);
}

void loop()
{
  OSCBundle bundleIN;
  int size;
  
  if ( (size = Udp.parsePacket())>0 ) {
    
    //Serial.println("received msg");
    while(size--)
       bundleIN.fill(Udp.read());

    bundleIN.route("/steer", onOscMessage);
  }

  // control servo
  servo.write(servoPos); 

  // control motor
  if (motorSpeed > 0) {
    motor->run(FORWARD);
    motor->setSpeed(motorSpeed);
  } else {
    motor->run(BACKWARD);
    motor->setSpeed(-motorSpeed);
  }
    
  // turn on motor
  delay(15);
}


void onOscMessage(OSCMessage &msg, int addrOffset ){
  servoPos = msg.getInt(0);
  motorSpeed = msg.getInt(1);
  
  Serial.print("servo: ");
  Serial.print(servoPos);
  Serial.print(", motor: ");
  Serial.println(motorSpeed);
}


void connectToWifi() {
  // check for the presence of the shield:
  if (WiFi.status() == WL_NO_SHIELD) {
    Serial.println("WiFi shield not present");
    // don't continue:
    while (true);
  }

  // attempt to connect to WiFi network:
  while ( status != WL_CONNECTED) {
    Serial.print("Attempting to connect to SSID: ");
    Serial.println(ssid);
    // Connect to WPA/WPA2 network. Change this line if using open or WEP network:
    status = WiFi.begin(ssid/*pass*/);

    // wait 10 seconds for connection:
    delay(5000);
  }

  Serial.println("Connected to wifi");
  printWiFiStatus();

  Serial.println("\nStarting connection to server...");
  Udp.begin(localPort);
  
}


void printWiFiStatus() {
  // print the SSID of the network you're attached to:
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());

  // print your WiFi shield's IP address:
  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);

  // print the received signal strength:
  long rssi = WiFi.RSSI();
  Serial.print("signal strength (RSSI):");
  Serial.print(rssi);
  Serial.println(" dBm");
}










