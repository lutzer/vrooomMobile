
void sliderSetup() {

  cp5.addSlider("cutOff")
    .setPosition(graphStartX, margin*1)
    .setSize(100, 20)
    .setRange(0, 1000)
    .setValue(250)
    ;    
    
  cp5.addSlider("maxValue")
    .setPosition(graphStartX +150, margin*1)
    .setSize(100, 20)
    .setRange(200, 600)
    .setValue(440)
    ;

  cp5.addSlider("speed")
    .setPosition(graphStartX, margin*2.5)
    .setSize(100, 20)
    .setRange(0, 10)
    .setValue(3)
    ;  

  cp5.addSlider("freqCut")
    .setPosition(graphStartX +150, margin*2.5)
    .setSize(100, 20)
    .setRange(0, 800)
    .setValue(800)
    ;  
    
   //cp5.addSlider("threshold")
   // .setPosition(graphStartX +300, margin*2.5)
   // .setSize(100, 20)
   // .setRange(0, 2.0)
   // .setValue(1.0)
   // ; 

}
