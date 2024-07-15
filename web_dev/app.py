from flask import Flask, request, render_template, jsonify
import serial
import signal
import sys
import cv2
import time
from picamera2 import Picamera2, Preview, MappedArray
import requests
import datetime
import sqlite3

import io
import logging
import socketserver
from http import server
import threading
from threading import Condition
import os
from shutil import copyfile

from picamera2.encoders import MJPEGEncoder
from picamera2.outputs import FileOutput

# Configuration of the network
server_address = '172.25.96.25'
image_port = '6000'

pi_address = '172.25.104.92'
stream_port = '5000'

target_server_url = f'http://{server_address}:{image_port}/upload'
stream_url1 = f'http://{pi_address}:{stream_port}/stream.mjpg'
stream_url2 = 'http://172.25.107.64:5000/video_feed'

# Streaming default website
PAGE = """\
<html>
<head>
<title>picamera2 MJPEG streaming demo</title>
</head>
<body>
<h1>Picamera2 MJPEG Streaming Demo</h1>
<img src="stream.mjpg" width="640" height="480" />
</body>
</html>
"""

class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()

class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True


# Create the Flask object
app = Flask(__name__)
# Initialize serial communication
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
# Global parameters
picam2 = None
output = None

# Send the camera image to the server 
def send_image(file_path, server_url):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d-%H%M%S")

    local_save_path = os.path.join('send_pictures/images', f'{current_time}.jpg')
    copyfile(file_path, local_save_path)

    with open(file_path, 'rb') as file:
        files = {'file': (f'{current_time}.jpg', file)}  # 使用当前时间作为文件名

        response = requests.post(server_url, files=files)
        print(response.text)


# Capture photo and send it to server
def capture_photo():  
    file_path = 'send_pictures/images/carPhoto.jpg'
    picam2.capture_file(file_path)
    time.sleep(1)
    send_image(file_path, target_server_url)
    return "Photo captured successfully"


@app.route('/', methods=['GET'])
def root():
    return render_template('index.html', info={"title": "Team 7 Vehicle", "stream_url1": stream_url1, "stream_url2": stream_url2}), 200

def get_records():
    # Connect to the SQLite database
    conn = sqlite3.connect('./database/cats.db')
    c = conn.cursor()

    # Query to select all records from the records table
    c.execute('SELECT * FROM records')

    # Fetch all results from the executed query
    rows = c.fetchall()

    # Close the connection
    conn.close()

    # Convert to list of dictionaries
    records = [{'id': row[0], 'filename': row[1], 'result': row[2]} for row in rows]
    
    return records

@app.route('/send_command', methods=['POST'])
def send_command():
    command = request.form['command']
    # Use 'p' to capture photos
    if command == 'p':
        response = capture_photo()
    elif command == 'save':
        # Connect to the SQLite database
        records = get_records()
        return jsonify({"last_command": command, "records": records})
    else:
        # send command to the vehicle's serial
        ser.write((command + '\n').encode('utf-8'))
        response = ser.readline().decode('utf-8').strip()

    return jsonify({"last_command": command, "response": response})

# Launch the streaming server
def run_streaming_server():
    address = ('', 5000)  # 改为端口 5000
    server = StreamingServer(address, StreamingHandler)
    server.serve_forever()

# Run the flask server
def run_flask_app():
    app.run(port=3237, host="0.0.0.0")

def main():
    global picam2, output
    
    # Initialize the camera
    picam2 = Picamera2()
    picam2.configure(picam2.create_video_configuration(main={"size": (640,480)}))
    output = StreamingOutput()
    picam2.start_recording(MJPEGEncoder(), FileOutput(output))

    # Create and launch the threads
    streaming_thread = threading.Thread(target=run_streaming_server)
    flask_thread = threading.Thread(target=run_flask_app)

    streaming_thread.start()
    flask_thread.start()

    # wait the thread to end
    streaming_thread.join()
    flask_thread.join()

if __name__ == '__main__':
    try:
        main()
    finally:
        if picam2:
            picam2.stop_recording()

    app.run(port=3237, host="0.0.0.0")

