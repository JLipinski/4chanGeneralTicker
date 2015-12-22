/*
 *  DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
 *  Version 2, December 2004
 *
 *  Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>
 *
 *  Everyone is permitted to copy and distribute verbatim or modified
 *  copies of this license document, and changing it is allowed as long
 *  as the name is changed.
 *
 *  DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
 *  TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
 *
 *  0. You just DO WHAT THE FUCK YOU WANT TO.
 */

#include <SPI.h>
#include <Adafruit_GFX.h>
#include <avr/pgmspace.h>
#include <Max72xxPanel.h>

const int PROGMEM pinCS = 10; // Attach CS to this pin, DIN to MOSI and CLK to SCK (cf http://arduino.cc/en/Reference/SPI )
const int PROGMEM numberOfHorizontalDisplays = 8;
const int PROGMEM numberOfVerticalDisplays = 1;

Max72xxPanel matrix = Max72xxPanel(pinCS, numberOfHorizontalDisplays, numberOfVerticalDisplays);

String tape = "Arduino";
const int PROGMEM wait = 15; // In milliseconds

String inputString = "";         // a string to hold incoming data
boolean stringComplete = false;  // whether the string is complete

const int PROGMEM spacer = 1;
const int PROGMEM width = 5 + spacer; // The font width is 5 pixels

void setup() {
  Serial.begin(9600);
  // reserve 200 bytes for the inputString:
  inputString.reserve(700);
  tape.reserve(700);

  matrix.setIntensity(1); // Use a value between 0 and 15 for brightness

  for (int i = 0; i < 8; i++) {
    matrix.setPosition(i, 7-i, 0);
  }
}

void loop() {
  if (stringComplete) {
    tape = inputString;
    inputString = "";
    stringComplete = false;
  }

  for ( int i = 0 ; i < width * tape.length() + matrix.width() - 1 - spacer; i++ ) {

    matrix.fillScreen(LOW);

    int letter = i / width;
    int x = (matrix.width() - 1) - i % width;
    int y = (matrix.height() - 8) / 2; // center the text vertically

    while ( x + width - spacer >= 0 && letter >= 0 ) {
      if ( letter < tape.length() ) {
        matrix.drawChar(x, y, tape[letter], HIGH, LOW, 1);
      }

      letter--;
      x -= width;
    }

    matrix.write(); // Send bitmap to display
    delay(wait);
    serialEvent();
  }
}

void serialEvent() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    if (inChar == '\n') {
      stringComplete = true;
      return;
    } else {
      inputString += inChar;
    }
  }
}

