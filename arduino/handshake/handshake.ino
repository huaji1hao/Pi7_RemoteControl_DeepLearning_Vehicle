// Pi to Arduino Serial Communication Test with Handshake

void setup() {
  // initialize both serial ports:
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }

  // Handshake process
  while (true) {
    if (Serial.available() > 0) {
      String handshake = Serial.readStringUntil('\n');
      if (handshake == "START") { // Start handshake signal
        Serial.println("ACK"); // Acknowledge signal
        break;
      }
    }
  }

  // Check for handshake confirmation
  while (true) {
    if (Serial.available() > 0) {
      String confirm = Serial.readStringUntil('\n');
      if (confirm == "CONFIRM") { // Confirmation signal
        break;
      }
    }
  }
}

void loop() {
  // Main loop for data communication
  while (true) {
    // read from serial, send back
    if (Serial.available() > 0) {
      int inByte = Serial.read();
      Serial.write(inByte); // Echo back the received byte
    }
  }
}
