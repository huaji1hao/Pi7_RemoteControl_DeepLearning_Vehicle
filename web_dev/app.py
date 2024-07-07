from flask import Flask, request, render_template
import serial

# Create the Flask object
app = Flask(__name__)

# Initialize serial communication
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

@app.route('/', methods=['GET', 'POST'])
def root():
    last_command = None
    response = None
    if request.method == 'POST':
        last_command = request.form['command']
        command = last_command + '\n'
        ser.write(command.encode('utf-8'))
        response = ser.readline().decode('utf-8').strip()
    
    return render_template('index.html', info={"title": "Team 7 Vehicle"}, last_command=last_command, response=response), 200

def main():
    app.run(port=3237, host="0.0.0.0")

if __name__ == '__main__':
    main()
