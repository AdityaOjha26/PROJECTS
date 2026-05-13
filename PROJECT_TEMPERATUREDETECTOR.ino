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
  Serial.println("System Initialized - Monitoring Temp & Humidity...");
}

void loop() {
  // Reading humidity and temperature
  float h = dht.readHumidity();
  float t = dht.readTemperature();

  // Check if any reads failed
  if (isnan(h) || isnan(t)) {
    Serial.println("Reading Error! Check sensor connections.");
    return;
  }

  // Displaying both values on Serial Monitor
  Serial.print("Humidity: ");
  Serial.print(h);
  Serial.print("%  |  ");
  Serial.print("Temperature: ");
  Serial.print(t);
  Serial.println(" *C");

  // Logic for LEDs remains the same
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

  delay(2000); // DHT22 needs 2 seconds between reads
}