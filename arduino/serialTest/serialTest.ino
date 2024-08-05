// Pi to Arduino Serial Communication Test

void setup() {
// initialize both serial ports:
	Serial.begin(9600);
}
void loop() {
// read from port 0, send to port 3:
	if (Serial.available()) {
		int inByte = Serial.read();
		Serial.write(inByte);
	}
}
