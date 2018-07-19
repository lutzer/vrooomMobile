/**
 * oscP5broadcastClient by andreas schlegel
 * an osc broadcast client.
 * an example for broadcast server is located in the oscP5broadcaster exmaple.
 * oscP5 website at http://www.sojamo.de/oscP5
 */

import oscP5.*;
import netP5.*;


OscP5 oscP5;

/* a NetAddress contains the ip address and port number of a remote location in the network. */
NetAddress dest; 

PVector cursor;

void setup() {
  size(400,400);
  frameRate(25);
  
  /* create a new NetAddress. a NetAddress is used when sending osc messages
   * with the oscP5.send method.
   */
  
  /* the address of the osc broadcast server */
  dest = new NetAddress("172.16.1.27",2390);
  
  cursor = new PVector(width/2,height/2);
  ellipseMode(RADIUS);
  
}


void draw() {
  background(0);
  fill(255);
  ellipse(cursor.x,cursor.y,20,20);
  
  sendPosition(cursor.x,cursor.y);
}


void mouseDragged() 
{
  cursor.x = mouseX;
  cursor.y = mouseY;
}

void mouseReleased() {
  cursor.x = width/2;
  cursor.y = height/2;
}


void keyPressed() {
  OscMessage msg;
  switch(key) {
    case('c'):
      /* connect to the broadcaster */
      msg = new OscMessage("/servo");
      msg.add(5);
      oscP5.send(msg,dest);
      println("sent c");

  }  
}

void sendPosition(float x, float y) {
  
    x = constrain(x, 0, width);
    y = constrain(y, 0, height);
  
    int steerX = int( map(x, 0, width, 180, 0) );
    int steerY = int( map(y, 0, height, -255, 255) );
    
    print(steerX);
    print(":");
    println(steerY);
  
    OscMessage msg;
    msg = new OscMessage("/steer");
    msg.add(steerX);
    msg.add(steerY);
    oscP5.send(msg,dest);
}
