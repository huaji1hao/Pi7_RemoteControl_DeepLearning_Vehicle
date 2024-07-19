#include <AFMotor.h>
#include <Arduino.h>
#include <NewPing.h>

#define TRIGGER_PIN 30
#define ECHO_PIN 28
#define MAX_DISTANCE 400 // Maximum sensor distance is rated at 400-500cm.

#define left_track_PIN 22                
#define middle_track_PIN 24
#define right_track_PIN 52

NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE);

AF_DCMotor motor1(1);  
AF_DCMotor motor2(2);  
AF_DCMotor motor3(3);  
AF_DCMotor motor4(4);  

unsigned long startTime = 0;
unsigned long duration = 0;
bool isMoving = false;
bool indefiniteMove = false;

int sensor[3] = {0, 0, 0};     

void setup() {
  Serial.begin(9600);
  resetMotors(); // Initialize motors
}

void loop() {
  // Check for serial input
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n'); // Read input from serial
    parseCommand(input); // Parse the received command
  }

  // Check if the motor should stop after the duration
  if (isMoving && !indefiniteMove) {
    if (millis() - startTime >= duration) {
      stopMotors();
      isMoving = false;
    }
  }

  double front_distance = sonar.ping_cm();
  if(front_distance > 0 && front_distance < 10) {
    stopMotors();
    isMoving = false;
    indefiniteMove = false;
  }
}

// Parse the received command
void parseCommand(String input) {
  if (input.length() == 1) {
    // Handle single character commands
    char command = input.charAt(0);
    handleSingleCharacterCommand(command);
  } else if (input.startsWith("read_sensors")) {
    // Handle read sensor command
    readSensors();
  } else {
    // Handle motor commands
    parseMotorCommand(input);
  }
}

// Handle single character commands
void handleSingleCharacterCommand(char command) {
  int speed = getSpeed(2); // Default speed

  if (command == 'w' || command == 's' || command == 'a' || command == 'd') {
    stopMotors();
    executeCommand(command, speed);
  } else if (command == 'x' || command == 'X') {
    stopMotors();
  } else if (command == 'y') {
    // Do nothing, just a placeholder
  } else {
    Serial.println("Invalid single character");
  }
}

// Read sensor values and print to serial
void readSensors() {
  sensor[0] = digitalRead(left_track_PIN);
  sensor[1] = digitalRead(middle_track_PIN);
  sensor[2] = digitalRead(right_track_PIN);

  Serial.print(sensor[0]);
  Serial.print(",");
  Serial.print(sensor[1]);
  Serial.print(",");
  Serial.println(sensor[2]);
}

// Parse motor commands
void parseMotorCommand(String input) {
  int firstComma = input.indexOf(',');
  int secondComma = input.indexOf(',', firstComma + 1);
  int thirdComma = input.indexOf(',', secondComma + 1);

  if (firstComma != -1 && secondComma != -1 && thirdComma != -1) {
    String motor = input.substring(0, firstComma);
    String direction = input.substring(firstComma + 1, secondComma);
    int speed = input.substring(secondComma + 1, thirdComma).toInt();
    int time = input.substring(thirdComma + 1).toInt();

    uint8_t dir = (direction == "f") ? FORWARD : BACKWARD;

    if (motor == "l") {
      Serial.print("turn left, speed: ");
      Serial.print(speed);
      Serial.print(", time: ");
      Serial.println(time);
      turn_left(speed, time);
    } else if (motor == "r") {
      Serial.print("turn right, speed: ");
      Serial.print(speed);
      Serial.print(", time: ");
      Serial.println(time);
      turn_right(speed, time);
    } else if (motor == "f") {
      Serial.print("go forward, speed: ");
      Serial.print(speed);
      Serial.print(", time: ");
      Serial.println(time);
      go_forward(speed, time);
    } else if (motor == "b") {
      Serial.print("go back, speed: ");
      Serial.print(speed);
      Serial.print(", time: ");
      Serial.println(time);
      go_back(speed, time);
    }
  } else {
    Serial.println("Invalid motor command format");
  }
}

// Execute movement or turn based on command
void executeCommand(char command, int speed) {
  switch (command) {
    case 'w':
      Serial.println("Vehicle move forward a little bit");
      go_forward(speed, 100);
      break;
    case 's':
      Serial.println("Vehicle move backward a little bit");
      go_back(speed, 100);
      break;
    case 'a':
      Serial.println("Vehicle turn left a little bit");
      turn_left(getSpeed(3), 100);
      break;
    case 'd':
      Serial.println("Vehicle turn right a little bit");
      turn_right(getSpeed(3), 100);
      break;
  }
}

// Stop all motors
void stopMotors() {
  motor1.run(RELEASE);
  motor4.run(RELEASE);
  motor2.run(RELEASE);
  motor3.run(RELEASE);
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

// Turn left with speed and time
void turn_left(int speed, int time) {
  motor1.setSpeed(speed);
  motor1.run(FORWARD);
  motor4.setSpeed(speed);
  motor4.run(BACKWARD);
  motor2.setSpeed(speed);
  motor2.run(FORWARD);
  motor3.setSpeed(speed);
  motor3.run(BACKWARD);

  if (time == -1) {
    indefiniteMove = true;
  } else {
    startTime = millis();
    duration = time;
    isMoving = true;
    indefiniteMove = false;
  }
}

// Turn right with speed and time
void turn_right(int speed, int time) {
  motor1.setSpeed(speed);
  motor1.run(BACKWARD);
  motor4.setSpeed(speed);
  motor4.run(FORWARD);
  motor2.setSpeed(speed);
  motor2.run(BACKWARD);
  motor3.setSpeed(speed);
  motor3.run(FORWARD);

  if (time == -1) {
    indefiniteMove = true;
  } else {
    startTime = millis();
    duration = time;
    isMoving = true;
    indefiniteMove = false;
  }
}

// Go forward with speed and time
void go_forward(int speed, int time) {
  motor1.setSpeed(speed);
  motor1.run(BACKWARD);
  motor4.setSpeed(speed);
  motor4.run(FORWARD);
  motor2.setSpeed(speed);
  motor2.run(FORWARD);
  motor3.setSpeed(speed);
  motor3.run(BACKWARD);

  if (time == -1) {
    indefiniteMove = true;
  } else {
    startTime = millis();
    duration = time;
    isMoving = true;
    indefiniteMove = false;
  }
}

// Go back with speed and time
void go_back(int speed, int time) {
  motor1.setSpeed(speed);
  motor1.run(FORWARD);
  motor4.setSpeed(speed);
  motor4.run(BACKWARD);
  motor2.setSpeed(speed);
  motor2.run(BACKWARD);
  motor3.setSpeed(speed);
  motor3.run(FORWARD);

  if (time == -1) {
    indefiniteMove = true;
  } else {
    startTime = millis();
    duration = time;
    isMoving = true;
    indefiniteMove = false;
  }
}
