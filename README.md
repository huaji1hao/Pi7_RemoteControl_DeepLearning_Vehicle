# NUS 2024 SWS Pi_SmartGuide_Vehicle

[中文版 zh-CN](README.zh-CN.md)

## Project Overview

In the Robotics section, we utilized the Raspberry Pi and Arduino Mega 2560. The Raspberry Pi primarily uses its external camera plugin, which we later leveraged for image recognition and model judgment. The Arduino part integrates multiple functional modules such as LED display, motor control based on L239D, servo control, etc., achieving control over various aspects of robot movement. Additionally, we used serial communication to link the two parts.

This vehicle also includes deep learning model recognition, involving transmission protocols and communication, environment setup, web design, parameter adjustment, and fitting, among other tasks.

## Project Members

### Core Members

- **UESTC_FANGYUZHANG** (Robotics): Hardware module functionality design, serial communication design
- **UNNC_JUNFENGZHU** (Robotics): Motor driver encapsulation, web interaction design

## 💎 Technical Implementation

### Baseline

A manually driven vehicle can find hidden "cats" in the lab's maze, using the onboard Picamera for identification, determining the type of cat, and displaying the recognition results on the web, testing the vehicle's driving smoothness, recognition accuracy, and searching strategy.

- Used HTTP protocol to enable real-time communication between the large model and web video content, showing the vehicle's recognition results and accuracy for various cats.
- Implemented serial communication to control the vehicle on the web, listening to keyboard input via serial communication to control the basic movement of the vehicle.
- Used the Flask framework to synchronize the camera content on the Raspberry Pi with the web in the form of a video stream, achieving front-end and back-end interaction.
- Arduino encapsulated the vehicle driving logic, using differential control for vehicle turning, encapsulated serial receiving module, and layered control of vehicle forward, backward, and turning.

Implementation logic: Control the vehicle with WASD to find the cat, identify the type and display the accuracy in real-time in front of the cat photo, press "R" to record the recognition result to the database, press "X" to stop the vehicle immediately. In the end, due to the search strategy, we found only 6/8 cat photos, but the recognition success rate was 100%, which was a satisfactory completion.

### Advanced

Utilizing DL and robot-related technologies to meet the needs, focusing on service scenarios rather than implementation techniques.

#### Smart Guide Vehicle

Aims to provide an affordable and technologically advanced alternative for the visually impaired, replacing traditional guide dogs. The core goal of this project is to integrate multiple technologies, including deep learning, remote-controlled robots, precise navigation, and voice interaction, to guide the blind through known mapped areas with a smart vehicle.

- Line tracking using three tracking modules.
- Ultrasonic obstacle avoidance.
- Dijkstra algorithm for path planning; we input the start and end points in advance, and the vehicle automatically plans the optimal path to take you to your destination.
- Implementation logic: The vehicle (Raspberry Pi) communicates with the server via socket (app.py), navigates through (py_control.py), plans the shortest path with Dijkstra algorithm (trialmap.py), retrieves the distance to the next intersection (get_distance.py), and preemptively determines the next turn direction. It also obtains the current camera's black line tilt angle to determine whether the vehicle has turned correctly, preventing the vehicle from leaving the black line after turning and failing to proceed to the next step. Upon reaching the destination, it recognizes the endpoint line on the ground and stops, informing the user behind via voice (voice.py) that they have arrived.

## 🚀 Future Plans

### Donkeycar:

Utilize our encapsulated hardware operation logic, optimize serial communication delays, understand Donkeycar, drive the vehicle on a predetermined route, record the speed of the left and right wheels every second, take 20 photos per second (performed by Raspberry Pi), and input the recorded data into the large model for training (performed by the host). The training results are then returned to the Raspberry Pi, enabling the vehicle to run autonomously on the predetermined route, achieving fixed-route intelligent navigation.

### Project Expansion:

- Add obstacle avoidance optimization, calculate angles with a gyroscope to achieve precise PID control, making turning operations more accurate.
- Use a ten-way infrared module to optimize black line tracking, also introducing PID control, allowing the vehicle to turn smoothly and follow curves on the black line.

### More Advanced Technology - True Guide Robot Dog:

- Interactive handle ensures real-time interaction with the user, preventing unexpected situations.
- SLAM technology + onboard GPS technology can analyze and judge the surrounding terrain in real-time and plan the route in advance.
