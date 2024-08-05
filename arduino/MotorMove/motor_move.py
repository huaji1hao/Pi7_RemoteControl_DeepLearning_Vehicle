import serial #module for serial port communication

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

try:
    while 1:
        user = input() + '\n';
        ser.write(user.encode('utf-8'));
        response = ser.readline()
        print(response.decode('utf-8'))

except KeyboardInterrupt:
    ser.close()
