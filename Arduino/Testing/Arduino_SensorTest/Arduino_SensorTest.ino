const unsigned int pin_LED              = 13;  // the index of the LED pin, see circuit.pdf
const unsigned int pin_PT                = A5;  // PT analog input pin



void setup() {
  Serial.begin(115200);  // USB connection to PC
  Serial.println();  // warm up the serial port

  // initialize the lightEmitterLED pin as an output:
  pinMode(pin_LED, OUTPUT);
  pinMode(pin_PT, INPUT);

  digitalWrite(pin_LED, HIGH);
}

void loop() {

  int reading = analogRead(pin_PT);
  Serial.println(reading);

  delay(50);
}
