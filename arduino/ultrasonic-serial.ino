// Wiring configuration
#define ECHO_PIN 8
#define TRIGGER_PIN 9

// Baud rate for external consumption
#define SERIAL_BAUD 9600

void setup()
{

	pinMode(TRIGGER_PIN, OUTPUT);
	pinMode(ECHO_PIN, INPUT);
	Serial.begin(SERIAL_BAUD);
}

void loop()
{
	float distance = ultrasonic_read(ECHO_PIN, TRIGGER_PIN);
	String serial_buffer = String(distance);
	serial_buffer = serial_buffer + "\n";

	Serial.print(serial_buffer);
}

float ultrasonic_read(int echoPin, int trigPin)
{
	// Clears the trigPin
	digitalWrite(trigPin, LOW);
	delayMicroseconds(2);

	// Sets the trigPin on HIGH state for 10 micro seconds
	digitalWrite(trigPin, HIGH);
	delayMicroseconds(10);
	digitalWrite(trigPin, LOW);

	// Reads the echoPin, returns the sound wave travel time in microseconds
	int duration = pulseIn(echoPin, HIGH);

	return duration * 0.034 / 2;
}
