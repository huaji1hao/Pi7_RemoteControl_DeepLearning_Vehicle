from flask import Flask, request, render_template, jsonify
import serial
import signal
import sys
import cv2
import time
from picamera2 import Picamera2, Preview, MappedArray
import requests
import datetime

target_server_url = 'http://172.25.96.208:5000/upload'

# Create the Flask object
app = Flask(__name__)
# Initialize serial communication
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

picam2 = Picamera2()
picam2.start()

@app.route('/', methods=['GET'])
def root():
    return render_template('index.html', info={"title": "Team 7 Vehicle"}), 200

@app.route('/send_command', methods=['POST'])
def capture_photo():  
    file_path = 'send_pictures/images/carPhoto.jpg'
    picam2.capture_file(file_path)
    time.sleep(1)
    send_image(file_path, target_server_url)
    return "Photo captured successfully"

def send_command():
    command = request.form['command']
    if command == 'p':
     # Trigger camera capture
        response = capture_photo()
    else:
        ser.write((command + '\n').encode('utf-8'))
        response = ser.readline().decode('utf-8').strip()

    return jsonify({"last_command": command, "response": response})

def send_image(file_path, server_url):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d-%H%M%S")
    with open(file_path, 'rb') as file:
        files = {'file': (f'{current_time}.jpg', file)}  # 使用当前时间作为文件名
        response = requests.post(server_url, files=files)
        print(response.text)

def main():
    app.run(port=3237, host="0.0.0.0")

if __name__ == '__main__':
    main()
