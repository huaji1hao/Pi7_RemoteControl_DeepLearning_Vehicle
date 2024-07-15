#include <AFMotor.h>
#include <NewPing.h>

#define TRIGGER_PIN 30
#define ECHO_PIN 28
#define MAX_DISTANCE 400 // Maximum sensor distance is rated at 400-500cm.

#define stop_car 0
#define go_forward 1
#define turn_left 2
#define turn_right 3
#define slow_down 4

NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE);

AF_DCMotor motor1(1);  
AF_DCMotor motor2(2);  
AF_DCMotor motor3(3);  
AF_DCMotor motor4(4); 

#define left_track_PIN 22                
#define middle_track_PIN 24
#define right_track_PIN 52

int sensor[3] = {0, 0, 0};                    
int state = stop_car;
int red_light_flag = 0;
int junction_cnt = 0;

typedef struct {
    int junction;
    char direction[20];
} junctionInfo;

// 路径定义为全局变量
junctionInfo ab[10];
junctionInfo ac[10];
junctionInfo ad[10];
junctionInfo ae[10];
junctionInfo af[10];

junctionInfo* current_path = NULL;
char current_path_name[3] = {'\0', '\0', '\0'}; // 初始化为空路径

// PID参数
double Kp = 1.0;  // 比例系数
double Ki = 0.0;  // 积分系数
double Kd = 0.0;  // 微分系数

double lastError = 0.0;
double integral = 0.0;

void setup() {
    Serial.begin(9600); 
    track_pinint();     
    define_paths(); // 定义路径
}

void loop() {
    read_sensor_values();
    motor_control();   
}

void define_paths() {
    // 示例路径
    strcpy(ab[0].direction, "turn_right"); // junction1: right

    strcpy(ac[0].direction, "turn_left");  // junction1: left

    strcpy(ad[0].direction, "go_forward"); // junction1: straight
    strcpy(ad[1].direction, "turn_left");  // junction2: left
    strcpy(ad[2].direction, "turn_right"); // junction3: right

    strcpy(ae[0].direction, "go_forward"); // junction1: straight
    strcpy(ae[1].direction, "go_forward"); // junction2: straight
    strcpy(ae[2].direction, "turn_right"); // junction3: right
    strcpy(ae[3].direction, "turn_left");  // junction4: left

    strcpy(af[0].direction, "go_forward"); // junction1: straight
    strcpy(af[1].direction, "go_forward"); // junction2: straight
    strcpy(af[2].direction, "go_forward"); // junction3: straight
}

void track_pinint(void) {
    pinMode(left_track_PIN, INPUT); 
    pinMode(middle_track_PIN, INPUT);
    pinMode(right_track_PIN, INPUT); 
}

void read_sensor_values() {
    sensor[0] = digitalRead(left_track_PIN);
    sensor[1] = digitalRead(middle_track_PIN);
    sensor[2] = digitalRead(right_track_PIN);
    char command = '\0';
    double front_distance = sonar.ping_cm();

    if (Serial.available() > 0) {
      String input = Serial.readStringUntil('\n');
      if (input.length() == 2) {
        current_path_name[0] = input.charAt(0);
        current_path_name[1] = input.charAt(1);
        current_path_name[2] = '\0'; // 确保末尾是空字符
        set_current_path(); // 设置当前路径
        state = go_forward; // 开始运动
      } else {
        command = input.charAt(0);
      }
    }

    if(front_distance > 0 && front_distance < 10) {
        state = stop_car; // obstacle detected
        return;
    }

    if(command =='l'){
        state = turn_left; // turn left command
        Serial.println("command driving: turn left");
    } else if(command == 'r'){
        state = turn_right; // turn right command
        Serial.println("command driving: turn right");
    } else if(command == 's'){
        state = slow_down; // yellow light
        Serial.println("command driving: yellow light, slow down");
    } else if(command == 'x'){
        red_light_flag = 1; // red light
        Serial.println("command driving: red light, stop");
    } else if(command == 'g'){
        red_light_flag = 0; // green light
        Serial.println("command driving: green light, go");
    } else if (current_path != NULL && 
               sensor[0] == 0 && sensor[1] == 1 && sensor[2] == 0) {
        if(red_light_flag == 1) state = stop_car; // red light
        else state = go_forward; // middle sensor detects black line
    } else if (current_path != NULL && 
               sensor[0] == 1 && sensor[1] == 1 && sensor[2] == 1) {
        // left or right sensor detects black line
        stopMotors();
        delay(500);
        execute_path(junction_cnt++); // 执行当前路径
    } else if (sensor[0] == 0 && sensor[1] == 0 && sensor[2] == 0){
        state = stop_car;
    } 
    else {
        state = stop_car;
    }
}

void set_current_path() {
    junction_cnt = 0;
    if (strcmp(current_path_name, "ab") == 0) {
        current_path = ab;
    } else if (strcmp(current_path_name, "ac") == 0) {
        current_path = ac;
    } else if (strcmp(current_path_name, "ad") == 0) {
        current_path = ad;
    } else if (strcmp(current_path_name, "ae") == 0) {
        current_path = ae;
    } else if (strcmp(current_path_name, "af") == 0) {
        current_path = af;
    } else {
        // 未知路径，默认停止
        current_path = NULL;
    }
    Serial.print("Set path: ");
    if(current_path == NULL) Serial.println("NULL");
    else Serial.println(current_path_name);
}

void execute_path(int junction) {
    if (current_path == NULL || junction > 9) return; // 防止越界或路径为空
    if (strcmp(current_path[junction].direction, "turn_left") == 0) {
        state = turn_left;
        Serial.println("auto driving: turn left");
    } else if (strcmp(current_path[junction].direction, "turn_right") == 0) {
        state = turn_right;
        Serial.println("auto driving: turn right");
    } else if (strcmp(current_path[junction].direction, "go_forward") == 0) {
        state = go_forward;
        Serial.println("auto driving: go straight");
    }
}

void motor_control() {
    if (state == stop_car) {
        stopMotors();
    } else if(state == turn_left) {
        turnMotor(getSpeed(3), FORWARD, BACKWARD);
    } else if(state == turn_right) {
        turnMotor(getSpeed(3), BACKWARD, FORWARD);
    } else if (state == go_forward) {
        pid_control();
    } else if (state == slow_down) {
        moveMotor(getSpeed(1), getSpeed(1), BACKWARD, FORWARD);
    }
}

void pid_control() {
    // 假设传感器返回的值：左传感器为0，中间传感器为1，右传感器为2
    int Kd=0,Ki=0,Kp=1.0;
    int position = sensor[0] * -1 + sensor[2] * 1;
    double error = position;
    integral += error;
    double derivative = error - lastError;
    double correction = Kp * error + Ki * integral + Kd * derivative;
    
    Serial.println(correction);

    int baseSpeed = getSpeed(2);
    int leftMotorSpeed = baseSpeed + correction;
    int rightMotorSpeed = baseSpeed - correction;

    moveMotor(leftMotorSpeed, rightMotorSpeed, BACKWARD, FORWARD);

    lastError = error;
}

void moveMotor(int l_speed, int r_speed, uint8_t leftDir, uint8_t rightDir) {
  motor1.setSpeed(l_speed);
  motor1.run(leftDir);
  motor4.setSpeed(l_speed);
  motor4.run(rightDir);
  motor2.setSpeed(r_speed);
  motor2.run(rightDir);
  motor3.setSpeed(r_speed);
  motor3.run(leftDir);
}

void stopMotors() {
  motor1.run(RELEASE);
  motor4.run(RELEASE);
  motor2.run(RELEASE);
  motor3.run(RELEASE);
}

int getSpeed(int speedSetting) {
  switch (speedSetting) {
    case 1:
      return 42; // Slow speed
    case 2:
      return 85; // Medium speed
    case 3:
      return 170; // Full speed
    default:
      return 85; // Default to medium speed
  }
}

 void turnMotor(int speed, uint8_t leftDir, uint8_t rightDir) {
  motor1.setSpeed(speed);
  motor1.run(leftDir);
  motor4.setSpeed(speed);
  motor4.run(rightDir);
  motor2.setSpeed(speed);
  motor2.run(leftDir);
  motor3.setSpeed(speed);
  motor3.run(rightDir);

  delay(650); // 调整这个延迟以实现完美的90度转弯

  stopMotors();
}