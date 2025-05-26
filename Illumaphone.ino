#include <LiquidCrystal.h>
#include <SoftwareSerial.h>

LiquidCrystal lcd(9, 8, 5, 4, 3, 2);

//Light sensor analog pins
const int analogPin1 = A0;
const int analogPin2 = A1;

const int numSamples = 10;

//SoftwareSerial for receiving Pitch from Arduino 3
const int rxFromA2 = 7; 
const int txUnused2 = 0;
SoftwareSerial softSerialFromA2(rxFromA2, txUnused2); //Only RX used

unsigned long lastSampleTime = 0;
unsigned long lastReadTime = 0;
const unsigned long sampleInterval = 5;
const unsigned long printInterval = 100;

int sampleCount = 0;
long sum1 = 0;
long sum2 = 0;

const String message = " Ambient Piano & Fantasy Harp    ";
unsigned long lastScrollTime = 0;
const unsigned long scrollInterval = 550;
int scrollIndex = 0;

String pitchDisplay = "Pitch 100%";

void setup() 
{
  Serial.begin(9600);          
  softSerialFromA2.begin(9600); //Receive pitch updates from Arduino 3
  
  lcd.begin(16, 2);
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Music Arduino!");
}

void loop() 
{
  unsigned long now = millis();

  if (now - lastSampleTime >= sampleInterval && sampleCount < numSamples) 
  {
    sum1 += analogRead(analogPin1);
    sum2 += analogRead(analogPin2);
    sampleCount++;
    lastSampleTime = now;
  }

  if (sampleCount >= numSamples && now - lastReadTime >= printInterval) 
  {
    int avg1 = sum1 / numSamples;
    int avg2 = sum2 / numSamples;

    sum1 = 0;
    sum2 = 0;
    sampleCount = 0;
    lastReadTime = now;
  }

  if (softSerialFromA2.available()) {
    String input = softSerialFromA2.readStringUntil('\n');
    input.trim();
    if (input.startsWith("PITCH:")) {
      pitchDisplay = "Pitch: " + input.substring(6) + "%";
    }
  }

  if (now - lastScrollTime >= scrollInterval) 
  {
    lcd.setCursor(0, 0);

    String displayText;
    if (scrollIndex + 16 <= message.length()) {
      displayText = message.substring(scrollIndex, scrollIndex + 16);
    } else {
      displayText = message.substring(scrollIndex) + message.substring(0, 16 - (message.length() - scrollIndex));
    }
    lcd.print(displayText);

    lcd.setCursor(0, 1);
    lcd.print(pitchDisplay);
    lcd.print("    "); //Extra spaces to erase leftovers

    scrollIndex++;
    if (scrollIndex >= message.length()) {
      scrollIndex = 0;
    }

    lastScrollTime = now;
  }
}
