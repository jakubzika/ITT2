
#include <NewPing.h>

#define SONAR_NUM     6 // Number of sensors.
#define MAX_DISTANCE 100 // Maximum distance (in cm) to ping.
#define PING_INTERVAL 40 // Milliseconds between sensor pings (29ms is about the min to avoid cross-sensor echo).
int dis =80;

int period = 15000; //led ON time  
unsigned long time_now = 0;


int led_0 = 3;         // the PWM pin the LED is attached to
int led_1 = 5;         // the PWM pin the LED is attached to
int led_2 = 6;         // the PWM pin the LED is attached to
int led_3 = 9;         // the PWM pin the LED is attached to
int led_4 = 10;         // the PWM pin the LED is attached to
int led_5 = 11;         // the PWM pin the LED is attached to



int brightness_0 = 0;  // how bright the LED is
int brightness_1 = 0;  // how bright the LED is
int brightness_2 = 0;  // how bright the LED is
int brightness_3 = 0;  // how bright the LED is
int brightness_4 = 0;  // how bright the LED is
int brightness_5 = 0;  // how bright the LED is

int fadeAmount = 5;  // how many points to fade the LED by


int time_count = 0;

unsigned long pingTimer[SONAR_NUM]; // Holds the times when the next ping should happen for each sensor.
unsigned int cm[SONAR_NUM];         // Where the ping distances are stored.
uint8_t currentSensor = 0;          // Keeps track of which sensor is active.
unsigned int  sensors[SONAR_NUM];

NewPing sonar[SONAR_NUM] = {     // Sensor object array.

  NewPing(2, 2, MAX_DISTANCE), // Each sensor's trigger pin, echo pin, and max distance to ping.
  NewPing(4, 4, MAX_DISTANCE),
  NewPing(7, 7, MAX_DISTANCE),
  NewPing(8, 8, MAX_DISTANCE),
  NewPing(12, 12, MAX_DISTANCE),
  NewPing(13, 13, MAX_DISTANCE)

};


void setup() {
  Serial.begin(9600); // Starts the serial communication

DDRD |=B11111000;

  pingTimer[0] = millis() + 75;           // First ping starts at 75ms, gives time for the Arduino to chill before starting.
  for (uint8_t i = 1; i < SONAR_NUM; i++) // Set the starting time for each sensor.
    pingTimer[i] = pingTimer[i - 1] + PING_INTERVAL;
}

void loop() {
  
  
  
  for (uint8_t i = 0; i < SONAR_NUM; i++) { // Loop through all the sensors.
    if (millis() >= pingTimer[i]) {         // Is it this sensor's time to ping?
      pingTimer[i] += PING_INTERVAL * SONAR_NUM;  // Set next time this sensor will be pinged.
      
      Serial.print("Dist0:");
      Serial.print(cm[0]);
      Serial.print(",");

      Serial.print("Dist1:");
      Serial.print(cm[1]);
      Serial.print(",");
      
      Serial.print("Dist2:");
      Serial.print(cm[2]);
      Serial.print(",");

      Serial.print("Dist3:");
      Serial.print(cm[3]);
      Serial.print(",");

      Serial.print("Dist4:");
      Serial.print(cm[4]);
      Serial.print(",");

      Serial.print("Dist5:");
      Serial.println(cm[5]);
      
      time_count = 0;

    

    
      
      sonar[currentSensor].timer_stop();          // Make sure previous timer is canceled before starting a new ping (insurance).
      currentSensor = i;                          // Sensor being accessed.
      cm[currentSensor] = 100;                      // Make distance zero in case there's no ping echo for this sensor.
      sonar[currentSensor].ping_timer(echoCheck); // Do the ping (processing continues, interrupt will call echoCheck to look for echo).
    
    }
  }
  /*
  brightness_0 = map(cm[4], 0, 100, 0, 255);
  analogWrite(led_0, brightness_0);

  brightness_1 = map(cm[0], 0, 100, 0, 255);
  analogWrite(led_1, brightness_1);
  
  brightness_2 = map(cm[1], 0, 100, 0, 255);
  analogWrite(led_2, brightness_2);
  
  brightness_3 = map(cm[2], 0, 100, 0, 255);
  analogWrite(led_3, brightness_3);
  
  brightness_4 = map(cm[3], 0, 100, 0, 255);
  analogWrite(led_4, brightness_4);

  brightness_5 = map(cm[5], 0, 100, 0, 255);
  analogWrite(led_5, brightness_5);
  */

  brightness_0 = map(cm[5], 0, 100, 0, 255);
  analogWrite(led_0, brightness_0);

  brightness_1 = map(cm[0], 0, 100, 0, 255);
  analogWrite(led_1, brightness_1);
  
  brightness_2 = map(cm[1], 0, 100, 0, 255);
  analogWrite(led_2, brightness_2);
  
  brightness_3 = map(cm[4], 0, 100, 0, 255);
  analogWrite(led_3, brightness_3);
  
  brightness_4 = map(cm[3], 0, 100, 0, 255);
  analogWrite(led_4, brightness_4);

  brightness_5 = map(cm[2], 0, 100, 0, 255);
  analogWrite(led_5, brightness_5);
  //delay(100);
  
}

void echoCheck() 
{ // If ping received, set the sensor distance to array.
  if (sonar[currentSensor].check_timer())
    cm[currentSensor] = sonar[currentSensor].ping_result / US_ROUNDTRIP_CM;
}

