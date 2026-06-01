#include <Arduino.h>
#include <Servo.h>
#include <Stepper.h>

#define SERVO_COUNT 5

// set start byte
const uint8_t START_BYTE = 0xEA;

// initialize servos
Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;
Servo servo5;
// initialize stepper
const int stepsPerRevolution = 2048;
Stepper Stepper1 = Stepper(stepsPerRevolution, 10, 12, 11, 13);

enum states_t {
  WAIT_START = 0,
  WAIT_READ_ANGLE0 = 1,
  WAIT_READ_ANGLE1 = 2,
  WAIT_READ_ANGLE2 = 3,
  WAIT_READ_ANGLE3 = 4,
  WAIT_READ_ANGLE4 = 5,
  WAIT_READ_STEPPER = 6,
};
  
states_t state = WAIT_START;
uint8_t angle[SERVO_COUNT] = {60, 60, 90, 80, 10}; // define start position
uint8_t preangle[SERVO_COUNT]  = {60, 60, 90, 80, 10};
uint8_t step = 0;
int i;

//servo control loop
// void servoSpeed(Servo servo, int servo_count) {
//   int servo1PPos = preangle[servo_count];
//   int servo1Pos = angle[servo_count]; //pos;
//
//       if (servo1PPos > servo1Pos) {
//         for ( int j = servo1PPos; j >= servo1Pos; j--) {   // Run servo down
//           servo.write(j);
//           delay(20);    // defines the speed at which the servo rotates
//         }
//       }
//       // If previous position is smaller then current position
//       if (servo1PPos < servo1Pos) {
//         for ( int j = servo1PPos; j <= servo1Pos; j++) {   // Run servo up
//           servo.write(j);
//           delay(20);
//         }
//       }
//       servo1PPos = servo1Pos;   // set current position as previous position
//       preangle[servo_count] = servo1PPos;
// }

// void servoSpeed(Servo servo, int servo_count) {
//
//       if (preangle[servo_count] > angle[servo_count]) {
//         for ( int j = preangle[servo_count]; j >= angle[servo_count]; j--) {   // Run servo down
//           servo.write(j);
//           delay(20);    // defines the speed at which the servo rotates
//         }
//       }
//       // If previous position is smaller then current position
//       if (preangle[servo_count] < angle[servo_count]) {
//         for ( int j = preangle[servo_count]; j <= angle[servo_count]; j++) {   // Run servo up
//           servo.write(j);
//           delay(20);
//         }
//       }
//       preangle[servo_count] = angle[servo_count];   // set current position as previous position
// }


void servoSpeed(Servo servo, int servo_count) {

      if (preangle[servo_count] > angle[servo_count]) {
          servo.write(preangle[servo_count] - 1); // Run servo down by one steppreangle[servo_count]
          preangle[servo_count] -= 1;
          delay(20);
        }
      }
      // If previous position is smaller then current position
      if (preangle[servo_count] < angle[servo_count]) {
          servo.write(preangle[servo_count] + 1); // Run servo up by one step
          preangle[servo_count] += 1;
          delay(20);
        }
      }
      //preangle[servo_count] = angle[servo_count];   // set current position as previous position
}



void setup() {

  Serial.begin(9600);

  servo1.attach(5);
  servo2.attach(6);
  servo3.attach(7);
  servo4.attach(8);
  servo5.attach(9);
  
  Stepper1.setSpeed(10);
}

void loop() {

  //get and read bytearray
  enum states_t next_state[] = {
    /* WAIT_START */       WAIT_READ_ANGLE0,
    /* WAIT_READ_ANGLE0 */ WAIT_READ_ANGLE1,
    /* WAIT_READ_ANGLE1 */ WAIT_READ_ANGLE2,
    /* WAIT_READ_ANGLE2 */ WAIT_READ_ANGLE3,
    /* WAIT_READ_ANGLE3 */ WAIT_READ_ANGLE4,
    /* WAIT_READ_ANGLE4 */ WAIT_READ_STEPPER,
    /* WAIT_READ_STEPPER */ WAIT_START
  };

  if (Serial.available()) {
    uint8_t event = 0;
    event = Serial.read();
    switch (state) {
      case WAIT_START:
        if (START_BYTE == event) {
          i = 0;
          state = next_state[state];
        }
        else {
          /* do nothing; remain in WAIT_START */
        }
        break;
      case WAIT_READ_ANGLE0:
      case WAIT_READ_ANGLE1:
      case WAIT_READ_ANGLE2:
      case WAIT_READ_ANGLE3:
      case WAIT_READ_ANGLE4:
        angle[i] = event;
        i += 1;
        state = next_state[state];
        break;
      case WAIT_READ_STEPPER:
        step = event;
        state = next_state[state];
        break;
      default:
        break;
    }
  }
  // positions for servos are saved in angle[i] (i=0-4) and stepps for stepper in step

//   servo1.write(angle[0]);
//   servo2.write(angle[1]);
//   servo3.write(angle[2]);
//   servo4.write(angle[3]);
//   servo5.write(angle[4]);

//   servoSpeed(servo1, 0, angle[0]);
//   servoSpeed(servo2, 1, angle[1]);
//   servoSpeed(servo3, 2, angle[2]);
//   servoSpeed(servo4, 3, angle[3]);
//   servoSpeed(servo5, 4, angle[4]);

  servoSpeed(servo1, 0);
  servoSpeed(servo2, 1);
  servoSpeed(servo3, 2);
  servoSpeed(servo4, 3);
  servoSpeed(servo5, 4);


  int stepmove = 20;

  if (step == 1) {
    Stepper1.step(stepmove);
    //Stepper1.step(0);
  }
  if (step == 2) {
    Stepper1.step(-stepmove);
    //Stepper1.step(0);
  }
  if (step == 0) {
    Stepper1.step(0);
  }

}
