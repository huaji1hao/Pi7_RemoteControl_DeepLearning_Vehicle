import serial
import threading
import time

class ArduinoController:
    def __init__(self, port='/dev/ttyACM0', baud_rate=9600):
        self.serial_connection = serial.Serial(port, baud_rate, timeout=1)
        self.running = True
        self.thread = threading.Thread(target=self._capture_and_send)
        self.thread.start()

    def _capture_and_send(self):
        while self.running:
            if self.controller.command:
                self.send_command(self.controller.command)
                time.sleep(0.1)

    def send_command(self, command):
        if command:
            self.serial_connection.write(f'{command}\n'.encode('utf-8'))
            response = self.serial_connection.readline()
            print(response.decode('utf-8'))

    def run(self, command):
        self.send_command(command)
    
    def close(self):
        self.serial_connection.close()
    
    def shutdown(self):
        self.running = False
        self.thread.join()
        self.close()



import threading
import time

class KeyboardController:
    def __init__(self):
        self.command = None
        self.running = True
        self.thread = threading.Thread(target=self._capture_input)
        self.thread.start()

    def _capture_input(self):
        import sys
        import termios
        import tty

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            while self.running:
                ch = sys.stdin.read(1)
                if ch in ['w', 'a', 's', 'd', 'x']:
                    self.command = ch
                time.sleep(0.1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    def run(self):
        return self.command

    def shutdown(self):
        self.running = False
        self.thread.join()
