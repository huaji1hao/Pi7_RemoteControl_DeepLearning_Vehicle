from flask import Flask, request, render_template, jsonify
import serial

# Create the Flask object
app = Flask(__name__)

# Initialize serial communication
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

@app.route('/', methods=['GET'])
def root():
    return render_template('index.html', info={"title": "Team 7 Vehicle"}), 200

@app.route('/send_command', methods=['POST'])
def send_command():
    command = request.form['command']
    ser.write((command + '\n').encode('utf-8'))
    response = ser.readline().decode('utf-8').strip()
    return jsonify({"last_command": command, "response": response})

def main():
    app.run(port=3237, host="0.0.0.0")

if __name__ == '__main__':
    main()
