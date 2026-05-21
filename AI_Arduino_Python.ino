#include "DHT.h"

#define DHTPIN 2       
#define DHTTYPE DHT22  

const int safeLed = 8;  
const int warnColor = 9; 
const int critColor = 10; 
const int buzzer = 11;

const float TEMP_WARN = 27.0;
const float TEMP_CRIT = 30.0;

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  pinMode(safeLed, OUTPUT);
  pinMode(warnColor, OUTPUT);
  pinMode(critColor, OUTPUT);
  pinMode(buzzer, OUTPUT);
  
  dht.begin();
  delay(3000); 
}

void loop() {
  float h = dht.readHumidity();
  float t = dht.readTemperature();

    if (isnan(h) || isnan(t)) {
    return;
  }

  Serial.print(t);
  Serial.print(",");
  Serial.println(h);

  if (t >= TEMP_CRIT) {
    digitalWrite(critColor, HIGH);
    digitalWrite(warnColor, LOW);
    digitalWrite(safeLed, LOW);
    tone(buzzer, 1000); 
  } 
  else if (t >= TEMP_WARN) {
    digitalWrite(critColor, LOW);
    digitalWrite(warnColor, HIGH);
    digitalWrite(safeLed, LOW);
    noTone(buzzer);
  } 
  else {
    digitalWrite(critColor, LOW);
    digitalWrite(warnColor, LOW);
    digitalWrite(safeLed, HIGH);
    noTone(buzzer);
  }

  delay(2000); // DHT22 2-second sampling rate
}
