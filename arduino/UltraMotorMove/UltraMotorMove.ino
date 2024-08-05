#include <AFMotor.h>
#include <Arduino.h>

AF_DCMotor motor1(1);  
AF_DCMotor motor2(2);  
AF_DCMotor motor3(3);  
AF_DCMotor motor4(4);  

const double pulsesPerCM = 0.11844; // Pulses per centimeter, adjust as needed

volatile int leftCount = 0; // Left wheel pulse count
volatile int rightCount = 0; // Right wheel pulse count
const int leftWE_PIN = 19; // Left encoder pin
const int rightWE_PIN = 18; // Right encoder pin

volatile bool isMoving = false; // Indicates if the vehicle is in motion
volatile char currentDirection = ' '; // Current direction of movement

// Interrupt service routines for counting pulses
void leftTick() {
  leftCount++;
}

void rightTick() {
  rightCount++;
}

void setup() {
  Serial.begin(9600);

  resetMotors(); // Initialize motors

  pinMode(leftWE_PIN, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(leftWE_PIN), leftTick, FALLING);

  pinMode(rightWE_PIN, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(rightWE_PIN), rightTick, FALLING);
}

void loop() {
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    char command = input.charAt(0);

    int speedSetting = 2; // Default to medium speed
    int speed = getSpeed(speedSetting);

    int distance = 15; // Fixed distance, adjust as needed
    int pulseCount = ceil(distance * pulsesPerCM);

    // Handle single-step movement commands
    if (command == 'w' || command == 's' || command == 'a' || command == 'd') {
      isMoving = false;
      stopMotors();
      executeCommand(command, speed, pulseCount);
    }
    // Handle continuous movement commands
    else if (command == 'W' || command == 'S' || command == 'A' || command == 'D') {
      isMoving = true;
      currentDirection = command;
    }
    // Handle stop command
    else if (command == 'x' || command == 'X') {
      isMoving = false;
      stopMotors();
    }


 


  // Execute continuous movement
  if (isMoving) {
    int speed = getSpeed(1);
    executeCommand(currentDirection, speed, -1); // -1 means continuous
  }
}

// Execute movement or turn based on command
void executeCommand(char command, int speed, int pulseCount) {
  switch (command) {
    case 'w':
    case 'W':
      moveMotor(speed, pulseCount, FORWARD, BACKWARD);
      break;
    case 's':
    case 'S':
      moveMotor(speed, pulseCount, BACKWARD, FORWARD);
      break;
    case 'a':
    case 'A':
      turnMotor(speed, pulseCount, FORWARD, BACKWARD);
      break;
    case 'd':
    case 'D':
      turnMotor(speed, pulseCount, BACKWARD, FORWARD);
      break;
  }
}

// Move the motors forward or backward
void moveMotor(int speed, int pulseCount, uint8_t leftDir, uint8_t rightDir) {
  leftCount = 0;
  rightCount = 0;

  motor1.setSpeed(speed);
  motor1.run(leftDir);
  motor4.setSpeed(speed);
  motor4.run(rightDir);
  motor2.setSpeed(speed);
  motor2.run(rightDir);
  motor3.setSpeed(speed);
  motor3.run(leftDir);

  if (pulseCount > 0) {
    waitForPulses(pulseCount);
    stopMotors();
  }
}

// Turn the motors left or right
void turnMotor(int speed, int pulseCount, uint8_t leftDir, uint8_t rightDir) {
  leftCount = 0;
  rightCount = 0;

  motor1.setSpeed(speed);
  motor1.run(leftDir);
  motor4.setSpeed(speed);
  motor4.run(rightDir);
  motor2.setSpeed(speed);
  motor2.run(leftDir);
  motor3.setSpeed(speed);
  motor3.run(rightDir);

  if (pulseCount > 0) {
    waitForPulses(pulseCount);
    stopMotors();
  }
}

// Wait until the pulse count reaches the target
void waitForPulses(int pulseCount) {
  while (leftCount < pulseCount && rightCount < pulseCount) {
    // Wait for counters to reach the target pulse count
  }
}

// Stop all motors
void stopMotors() {
  motor1.run(RELEASE);
  motor4.run(RELEASE);
  motor2.run(RELEASE);
  motor3.run(RELEASE);
  Serial.println("Motors stopped");
}

// Initialize all motors to stopped state
void resetMotors() {
  motor1.setSpeed(0);
  motor1.run(RELEASE);
  motor2.setSpeed(0);
  motor2.run(RELEASE);
  motor3.setSpeed(0);
  motor3.run(RELEASE);
  motor4.setSpeed(0);
  motor4.run(RELEASE);
}

// Get speed value based on the speed setting
int getSpeed(int speedSetting) {
  switch (speedSetting) {
    case 1:
      return 85; // Slow speed
    case 2:
      return 170; // Medium speed
    case 3:
      return 255; // Full speed
    default:
      return 170; // Default to medium speed
  }
}
