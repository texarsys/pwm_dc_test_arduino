int periodInput = 100;
int dcInput = 50;
int numberInput = 0;

int onTime = 0;
int offTime = 0;
int var_i = 0;

void setup() {
        Serial.begin(9600);     // opens serial port, sets data rate to 9600 bps
        pinMode(13, OUTPUT);
}

void loop() {

        digitalWrite(13, HIGH);
        delay(onTime);
        digitalWrite(13, LOW);
        //delayMicroseconds(offTime);
        delay(offTime);
  
  
        if (Serial.available() > 0) {

          //if the first character is 'p', it represents period in msec
          if (Serial.peek() == 'p') {
            delay(10);
            Serial.read();

            while (Serial.available() > 0) {
              numberInput *= 10;
              numberInput += (Serial.read()-'0');
              delay(10);
            }

            periodInput = numberInput;
            onTime = (long)periodInput * (long)dcInput / 100;
            offTime = periodInput - onTime;
            Serial.println(periodInput, DEC);
            Serial.println(dcInput, DEC);
            Serial.println(onTime, DEC);
            Serial.println(offTime, DEC);
            numberInput = 0;
            
          }

          //if the first character is 'd', it represents dutycycle in %
          if (Serial.peek() == 'd') {
            delay(10);
            Serial.read();

            while (Serial.available() > 0) {
              numberInput *= 10;
              numberInput += (Serial.read()-'0');
              delay(10);
            }

            dcInput = numberInput;
            onTime = (long)periodInput * (long)dcInput / 100;
            offTime = periodInput - onTime;

            Serial.println(periodInput, DEC);
            Serial.println(dcInput, DEC);
            Serial.println(onTime, DEC);
            Serial.println(offTime, DEC);
            numberInput = 0;
          }
          
          
        }


}

