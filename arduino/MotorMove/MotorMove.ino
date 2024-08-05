#include <AFMotor.h>

AF_DCMotor motor1(1);  
AF_DCMotor motor2(2);  
AF_DCMotor motor3(3);  
AF_DCMotor motor4(4);  

const double pulsesPerCM = 0.11844; // 每厘米对应的脉冲数，需要根据实际情况调整

volatile int leftCount = 0; // 左轮计数
volatile int rightCount = 0; // 右轮计数
const int leftWE_PIN = 19; // 左编码器引脚
const int rightWE_PIN = 18; // 右编码器引脚

void leftTick() {
  leftCount++;
}

void rightTick() {
  rightCount++;
}

void setup() {
  Serial.begin(9600);

  motor1.setSpeed(0);
  motor1.run(RELEASE);
  motor2.setSpeed(0);
  motor2.run(RELEASE);
  motor3.setSpeed(0);
  motor3.run(RELEASE);
  motor4.setSpeed(0);
  motor4.run(RELEASE);

  pinMode(leftWE_PIN, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(leftWE_PIN), leftTick, FALLING);

  pinMode(rightWE_PIN, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(rightWE_PIN), rightTick, FALLING);
}

void loop() {
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    char command = input.charAt(0);

    int speedSetting = 2; // 默认中速
    int speed = 0;
    switch (speedSetting) {
      case 1:
        speed = 85; // 慢速
        break;
      case 2:
        speed = 170; // 中速
        break;
      case 3:
        speed = 255; // 全速
        break;
    }

    int distance = 15; // 固定距离，您可以根据需要调整
    int pulseCount = ceil(distance * pulsesPerCM);

    if (command == 'w') {
      moveForward(speed, pulseCount);
    } else if (command == 's') {
      moveBackward(speed, pulseCount);
    } else if (command == 'a') {
      turnLeft(speed, pulseCount);
    } else if (command == 'd') {
      turnRight(speed, pulseCount/2);
    }
  }
}

void moveForward(int speed, int pulseCount) {
  leftCount = 0;
  rightCount = 0;

  motor1.setSpeed(speed);
  motor1.run(BACKWARD);
  motor4.setSpeed(speed);
  motor4.run(FORWARD);
  motor2.setSpeed(speed);
  motor2.run(FORWARD);
  motor3.setSpeed(speed);
  motor3.run(BACKWARD);

  while (leftCount < pulseCount && rightCount < pulseCount) {
    // 等待计数器达到目标脉冲数
  }

  motor1.run(RELEASE);
  motor4.run(RELEASE);
  motor2.run(RELEASE);
  motor3.run(RELEASE);
  Serial.println("Move forward complete");
}

void moveBackward(int speed, int pulseCount) {
  leftCount = 0;
  rightCount = 0;

  motor1.setSpeed(speed);
  motor1.run(FORWARD);
  motor4.setSpeed(speed);
  motor4.run(BACKWARD);
  motor2.setSpeed(speed);
  motor2.run(BACKWARD);
  motor3.setSpeed(speed);
  motor3.run(FORWARD);

  while (leftCount < pulseCount && rightCount < pulseCount) {
    // 等待计数器达到目标脉冲数
  }

  motor1.run(RELEASE);
  motor4.run(RELEASE);
  motor2.run(RELEASE);
  motor3.run(RELEASE);
  Serial.println("Move backward complete");
}

void turnLeft(int speed, int pulseCount) {
  leftCount = 0;
  rightCount = 0;

  motor1.setSpeed(speed);
  motor1.run(FORWARD);
  motor4.setSpeed(speed);
  motor4.run(BACKWARD);
  motor2.setSpeed(speed);
  motor2.run(FORWARD);
  motor3.setSpeed(speed);
  motor3.run(BACKWARD);

  while (leftCount < pulseCount && rightCount < pulseCount) {
    // 等待计数器达到目标脉冲数
  }

  motor1.run(RELEASE);
  motor4.run(RELEASE);
  motor2.run(RELEASE);
  motor3.run(RELEASE);
  Serial.println("Turn left complete");
}

void turnRight(int speed, int pulseCount) {
  leftCount = 0;
  rightCount = 0;

  

  motor1.setSpeed(speed);
  motor1.run(BACKWARD);
  motor4.setSpeed(speed);
  motor4.run(FORWARD);
  motor2.setSpeed(speed);
  motor2.run(BACKWARD);
  motor3.setSpeed(speed);
  motor3.run(FORWARD);

  while (leftCount < pulseCount && rightCount < pulseCount) {
    // 等待计数器达到目标脉冲数
  }

  motor1.run(RELEASE);
  motor4.run(RELEASE);
  motor2.run(RELEASE);
  motor3.run(RELEASE);
  Serial.println("Turn right complete");
}
