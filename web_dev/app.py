from flask import Flask, request, render_template, jsonify
import serial
import signal
import sys
import cv2
from picamera2 import Picamera2, Preview, MappedArray
# Create the Flask object
app = Flask(__name__)

# Initialize serial communication
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

@app.route('/', methods=['GET'])
def root():
    return render_template('index.html', info={"title": "Team 7 Vehicle"}), 200

@app.route('/send_command', methods=['POST'])
def send_command():
    order = input()
    command = request.form['command']
    if order == 'p':
        # Trigger camera capture
        capture_photo()
        response = "Camera captured a photo."
    else:
        ser.write((command + '\n').encode('utf-8'))
        response = ser.readline().decode('utf-8').strip()

    return jsonify({"last_command": command, "response": response})
 def capture_photo(save_path):
    camera = PiCamera()
    camera.resolution = (3280，2464)  # 设置摄像头分辨率，可以根据需要调整3280 × 2464
    camera.start_preview()
    time.sleep(2)  # 等待摄像头预热和自动调整
    camera.capture(save_path)
    camera.stop_preview()
    camera.close()
def main():
    app.run(port=3237, host="0.0.0.0")

if __name__ == '__main__':
    main()
