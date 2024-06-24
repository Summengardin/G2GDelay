// Setup pins to your liking
const int PHOTO_PIN = A5;
const int LED_PIN = 13;

unsigned int measurement_count = 25;
double measurements[100];

unsigned int current;
String command;

unsigned long threshold = 7;
unsigned long threshold_offset = 10;
unsigned long min = 0;
unsigned long max = 0;
unsigned long average = 0;

unsigned long start;
unsigned long end;
unsigned int i;


const unsigned int RANDOM_DELAY_MIN = 1000;
const unsigned int RANDOM_DELAY_MAX = 2000;
const unsigned int CALIBRATION_SAMPLES = 10;


const int s_IDLE = 0;
const int s_CALIBRATE = 1;
const int s_TEST_LIGHT = 2;
const int s_MEASUREMENT = 3;
int state = s_IDLE;

bool led_state = false;
bool is_calibrated = false;

bool running = false;


void LED_ON() {
  led_state = true;
  digitalWrite(LED_PIN, 1);
}

void LED_OFF() {
  led_state = false;
  digitalWrite(LED_PIN, 0);
}


void calibration() {
  LED_OFF();
  delay(100);
  LED_ON();
  delay(100);
  LED_OFF();
  delay(100);
  LED_ON();
  delay(100);

  LED_OFF();
  delay(2500); // Allowing for a 2.5 seconds maximum delay
  for (int i = 0; i < CALIBRATION_SAMPLES; i++){
    min += analogRead(PHOTO_PIN);
    delay(10);
  }
  min /= CALIBRATION_SAMPLES;
  

  LED_ON();
  delay(2500); // Allowing for a 2.5 seconds maximum delay
  for (int i = 0; i < CALIBRATION_SAMPLES; i++){
    max += analogRead(PHOTO_PIN);
    delay(10);
  }
  max /= CALIBRATION_SAMPLES;

  LED_OFF();

  /* Threshold is the minimum value increased by 10.
   *  
   * This might need to be adapted to the exact used LED. The lower the threshold is,
   * the less time is "wasted" for the LED to be bright enough. We are talking about
   * potentially 100us just  by increasing the threshold by 10.
   */

  if (min >= max)
  { 
    Serial.print("Error: min: ");
    Serial.print(min);
    Serial.print(" max: ");
    Serial.print(max);
    Serial.println(". Not enough light to calibrate. Calibration failed.");
    return;
  }
  
  if (max > min + threshold_offset)
  {
    threshold = min + threshold_offset;
  }
  else
  {
    threshold = int((max - min)/2 + min);
  }

  is_calibrated = true;



  Serial.print("Min: ");
  Serial.print(min);
  Serial.print(" Max: ");
  Serial.print(max);
  Serial.print(" Threshold: ");
  Serial.println(threshold);
}

void testLight() {

  LED_ON();
  double reading = takeMeasurement(); 
  Serial.println(reading/1000);
  Serial.println();

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
  LED_OFF();

  Serial.begin(115200);
  //Serial.println("#################");
  //Serial.println("1 - calibration");
  //Serial.println("2 - measurements");
  //Serial.println("#################");
}

void processSerial() {
  if(Serial.available() > 0) {
    command = Serial.readString();
    command.trim();

    if(command == "cali")
    { 
        Serial.println();
        threshold_offset = Serial.parseInt();
      //Serial.println("Running Calibration...");
        state = s_CALIBRATE;
        calibration();
        state = s_IDLE;
        return;
    }
    else if (command == "test_light")
    {
        state = s_TEST_LIGHT;
        Serial.println();
        return;
    }
    else if(command == "meas")
    {
      Serial.println();

      measurement_count = Serial.parseInt() + 1;


      //Serial.println("Running Measurements...");

        // Dummy read otherwise the first measurement is a bit off.
        //analogRead(photoPin);

        state = s_MEASUREMENT;
        
        current = 0;
        //startTimer();
    }
    else if(command == "light_on" and state == s_TEST_LIGHT)
    {
      LED_ON();
      Serial.println();
    }
    else if(command == "light_off" and state == s_TEST_LIGHT)
    {
      LED_OFF();
      Serial.println();
    }
    else if(command == "stop")
    {
      state = s_IDLE;
      LED_OFF();
    }
    else
    {
      // Serial.println("Could not parse Serial");
    }
  }
}

unsigned long takeMeasurement() {
  do {
    LED_ON();
    start = micros();
    while(analogRead(PHOTO_PIN) < threshold);
    end = micros();
    LED_OFF();
  } while(start > end); // Repeat the measuremtn if case the timer overflowed

  return end - start;
}


void loop() {
  processSerial();

  if (state == s_IDLE){
    LED_OFF();
  }
  if (state == s_CALIBRATE) {

  }
  else if (state == s_TEST_LIGHT) {
    Serial.println(analogRead(PHOTO_PIN));
    delay(100);
  }
  else if (state == s_MEASUREMENT) {
    double reading = takeMeasurement();
    measurements[current++] = reading;
    Serial.println(reading/1000);
    if(current >= measurement_count) {
      state = s_IDLE;
    } else {
      delay(random(RANDOM_DELAY_MIN, RANDOM_DELAY_MAX));
    }
  }
}




