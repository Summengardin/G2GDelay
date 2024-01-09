// Setup pins to your liking
const int PHOTO_PIN = A5;
const int LED_PIN = 13;

unsigned int measurement_count = 25;
double measurements[100];

unsigned int current;
String command;

unsigned long threshold = 7;
unsigned long min = 0;
unsigned long max = 0;
unsigned long average = 0;

unsigned long start;
unsigned long end;
unsigned int i;

const unsigned int RANDOM_DELAY_MIN = 1000;
const unsigned int RANDOM_DELAY_MAX = 2000;
const unsigned int CALIBRATION_SAMPLES = 10;

bool running = false;

void calibration() {
  digitalWrite(LED_PIN, 0);
  delay(100);
  digitalWrite(LED_PIN, 1);
  delay(100);
  digitalWrite(LED_PIN, 0);
  delay(100);
  digitalWrite(LED_PIN, 1);
  delay(100);

  digitalWrite(LED_PIN, 0);
  delay(2500); // Allowing for a 2.5 seconds maximum delay
  for (int i = 0; i < CALIBRATION_SAMPLES; i++){
    min += analogRead(PHOTO_PIN);
    delay(10);
  }
  min /= CALIBRATION_SAMPLES;
  

  digitalWrite(LED_PIN, 1);
  delay(2500); // Allowing for a 2.5 seconds maximum delay
  for (int i = 0; i < CALIBRATION_SAMPLES; i++){
    max += analogRead(PHOTO_PIN);
    delay(10);
  }
  max /= CALIBRATION_SAMPLES;

  digitalWrite(LED_PIN, 0);

  /* Threshold is the minimum value increased by 10.
   *  
   * This might need to be adapted to the exact used LED. The lower the threshold is,
   * the less time is "wasted" for the LED to be bright enough. We are talking about
   * potentially 100us just  by increasing the threshold by 10.
   */
  
  if (max > min + 10)
  {
      threshold = min + 10;
  } else
  {
    threshold = int((max - min)/2 + min);
  }



  Serial.print("Min: ");
  Serial.print(min);
  Serial.print(" Max: ");
  Serial.print(max);
  Serial.print(" Threshold: ");
  Serial.println(threshold);
}

void printResults() {
  average = 0;
  max = 0;  
  min = measurements[0];

  Serial.println("##### START #####");
  for(i = 0; i < measurement_count; i += 1) {
    if(measurements[i] > max) {
      max = measurements[i];
    }

    if(measurements[i] < min) {
      min = measurements[i];
    }
    
    average += measurements[i];
    if(i < 10) {
      Serial.print(0);
    }
    Serial.print(i);
    Serial.print(":\t");
    Serial.print(measurements[i]);
    Serial.print("us\t(");
    Serial.print(measurements[i] / 1000);
    Serial.println("ms)");
  }
  Serial.println("#################");
  Serial.print("Avg:\t");
  Serial.print(average / measurement_count);
  Serial.print("us\t(");
  Serial.print(average / measurement_count / 1000);
  Serial.println("ms)");
  Serial.print("Min:\t");
  Serial.print(min);
  Serial.print("us\t(");
  Serial.print(min / 1000);
  Serial.println("ms)");
  Serial.print("Max:\t");
  Serial.print(max);
  Serial.print("us\t(");
  Serial.print(max / 1000);
  Serial.print("ms)");
  Serial.println();
  
  Serial.println("#####  END  #####");
}

void setup() {
  pinMode(PHOTO_PIN, INPUT);

  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, 0);

  Serial.begin(115200);
  //Serial.println("#################");
  //Serial.println("1 - calibration");
  //Serial.println("2 - measurements");
  //Serial.println("#################");
}

void processSerial() {
  if(Serial.available() > 0) {
    command = Serial.readString();
    if(command == "cali")
    {
      //Serial.println("Running Calibration...");

        calibration();
        return;
    }
    else if(command == "meas")
    {
      Serial.println();

      measurement_count = Serial.parseInt() + 1;


      //Serial.println("Running Measurements...");

        // Dummy read otherwise the first measurement is a bit off.
        //analogRead(photoPin);

        running = true;
        current = 0;
        //startTimer();
    }

  }
}

unsigned long takeMeasurement() {
  do {
    digitalWrite(LED_PIN, 1);
    start = micros();
    while(analogRead(PHOTO_PIN) < threshold);
    end = micros();
    digitalWrite(LED_PIN, 0);
  } while(start > end); // Repeat the measuremtn if case the timer overflowed

  return end - start;
}

void loop() {
  processSerial();

  while(running) {
    double reading = takeMeasurement();
    measurements[current++] = reading;
    Serial.println(reading/1000);
    if(current >= measurement_count) {
      running = false;
      //printResults();

      return;
    }

    delay(random(RANDOM_DELAY_MIN, RANDOM_DELAY_MAX));
  }
}


