import serial # module for serial port communication
import time

# Open serial port
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

# Handshake process
def handshake():
    while True:
        ser.write(b'START\n') # Send handshake start signal
        time.sleep(1)
        if ser.in_waiting > 0:
            response = ser.readline().decode('utf-8').strip()
            if response == "ACK": # Acknowledge signal
                ser.write(b'CONFIRM\n') # Send confirmation signal
                return

handshake() # Perform handshake

try:
    while True:
        user = input() + '\n'
        ser.write(user.encode('utf-8'))
        response = ser.readline()
        print(response.decode('utf-8'))

except KeyboardInterrupt:
    ser.close()
