#include "SerialTransfer.h"
#define pot_1 A2 
#define pot_2 A3 
#define RST_PIN 9

SerialTransfer myTransfer;

struct sensor {
  float sensor_1;
  float sensor_2;
  
} sensorStruct;

struct pantilt {

  float pan;
  float tilt;
  
} pantiltStruct;



char arr[] = "hello";


void setup()
{
  SerialUSB.begin(115200);
  Serial1.begin(115200);
  myTransfer.begin(Serial1);
  analogReadResolution(12);
  sensorStruct.sensor_1 = 3.5;
  sensorStruct.sensor_2 = 4.5;
  pantiltStruct.pan = 60 ;
  pantiltStruct.tilt = 90;
}


void loop()
{
  // use this variable to keep track of how many
  // bytes we're stuffing in the transmit buffer
  float sensor_1 = analogRead(pot_1);
  float sensor_2 = analogRead(pot_2);
  sensorStruct.sensor_1 = sensor_1;
  sensorStruct.sensor_2 = sensor_2;
  uint16_t sendSize = 0;

  ///////////////////////////////////////// Stuff buffer with struct
  sendSize = myTransfer.txObj(sensorStruct, sendSize);

  ///////////////////////////////////////// Stuff buffer with array
//  sendSize = myTransfer.txObj(arr, sendSize);

  ///////////////////////////////////////// Send buffer
  myTransfer.sendData(sendSize);
    if(myTransfer.available())
  {
    // use this variable to keep track of how many
    // bytes we've processed from the receive buffer
    uint16_t recSize = 0;
    

    recSize = myTransfer.rxObj(pantiltStruct, recSize);
    float pan = pantiltStruct.pan;
    float tilt = pantiltStruct.tilt;
    SerialUSB.println(pan);
    SerialUSB.println(tilt);
    SerialUSB.println(recSize);
  }
  delay(100);
}
