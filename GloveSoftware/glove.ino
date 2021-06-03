/*
Software solution which reads Accelerometer,
Gyroscope and Magnetometer values
From the MPU-9250 motion sensor.
The raw data is then interpreted and flushed
In the serial port.
Software was built to be ran on the ESP32 architecture
And as a result, it’s compatibility has only been checked on
The ESP-32 based microcontrollers.
This code was uploaded to a ESP-32-WROOM microcontroller.
*/
#include <MPU9250_asukiaaa.h>
 
#ifdef _ESP32_HAL_I2C_H_
#define SDA_PIN 21
#define SCL_PIN 22
#endif
 
MPU9250_asukiaaa mySensor;

//Buttons are connected to pins D2 & D4
// i.e. pins 2 & 4
const int LMB_PIN = 4;
const int RMB_PIN = 2;

//Stores the state of the button in order
//to only send the it's state when it changes
int oldLMBState = 0;
int oldRMBState = 0;

//Moving the mouse if the values are higher than 
//the threshold
const int MOVE_THRESH = 18;
 
//Zero acceleration values read
//from the accelerometer for X & Y axis:
const int ZERO_X = 0;
const int ZERO_Y = 0;
 
//The maximum acceleration values possible
//from the accelerometer for X & Y axis:
const int MAX_X = 4096;
const int MAX_Y = 4096;
 
//The minimum acceleration values possible
//from the accelerometer for X & Y axis:
const int MIN_X = -4096;
const int MIN_Y = -4096;
 
//A value which states whether or not the axis should be inverted
const int INVERT_X = 1;
const int INVERT_Y = 1;
 
//The maximum speed of x and y axis
//i.e sensitivity
const int MAX_CURSOR_SPEED_MULTIPLIER = 50;  
 
// Sets the sleep timer, i.e
// the frequency in which the program
// reads and flushes the data
const int GLOBAL_DELAY = 100;
 
void setup() {
while(!Serial);
 
Serial.begin(115200);
Serial.println("System is operational");
 
#ifdef _ESP32_HAL_I2C_H_
// for esp32
Wire.begin(SDA_PIN, SCL_PIN); //sda, scl
#else
Wire.begin();
#endif
 
mySensor.setWire(&Wire);
 
mySensor.beginAccel();
mySensor.beginGyro();
mySensor.beginMag();
}
 
void loop() {

mySensor.gyroUpdate();
processAccelerometer(mySensor.gyroX(), mySensor.gyroY(), mySensor.gyroZ());

int LMBReading = digitalRead(LMB_PIN);
int RMBReading = digitalRead(RMB_PIN);

if(LMBReading != oldLMBState){
  Serial.println("LMB: " + String(LMBReading));
  oldLMBState = LMBReading;
  }
if(RMBReading != oldRMBState){
  Serial.println("RMB: " + String(RMBReading));
  oldRMBState = RMBReading;
  }

delay(GLOBAL_DELAY);
}


void processAccelerometer(int16_t XReading, int16_t YReading, int16_t ZReading){
  //Initi values for the final cursor movement.
  int16_t mouseMovementX = 0;
  int16_t mouseMovementY = 0;
  
  //Calculate mouse movement
  //If the analog X reading is ouside of the threshold
  if(MOVE_THRESH < abs( XReading - ZERO_X )){
    //calculate X mouse movement based on how far the X acceleration is from its zero value.
    mouseMovementX = ((((float)( 2 * MAX_CURSOR_SPEED_MULTIPLIER) / (MAX_X - MIN_X)) * (XReading - MIN_X)) - MAX_CURSOR_SPEED_MULTIPLIER) * INVERT_X;
  }
  else
  {
    //Within the threshold, the cursor does not move.
    mouseMovementX = 0;
  }
 
  //If the analog Y reading is ouside of the threshold 
  if(MOVE_THRESH < abs( YReading - ZERO_Y ) )
  {
    //calculate Y mouse movement based on how far the Y acceleration is from its zero value.
    mouseMovementY =  ((((float)(2 * MAX_CURSOR_SPEED_MULTIPLIER) / (MAX_Y - MIN_Y)) * (YReading - MIN_Y)) - MAX_CURSOR_SPEED_MULTIPLIER) * INVERT_Y;
  }
  else
  {
    //Within the threshold, the ursor does not move.
    mouseMovementY = 0;
  }
  Serial.println("mouseMovementX: " + String(mouseMovementX));
  Serial.println("mouseMovementY: " + String(mouseMovementY));
  Serial.flush();
}
