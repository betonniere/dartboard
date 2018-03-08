// Copyright (C) Yannick Le Roux.
// This file is part of Dartboard.
//
//   Dartboard is free software: you can redistribute it and/or modify
//   it under the terms of the GNU General Public License as published by
//   the Free Software Foundation, either version 3 of the License, or
//   (at your option) any later version.
//
//   Dartboard is distributed in the hope that it will be useful,
//   but WITHOUT ANY WARRANTY; without even the implied warranty of
//   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//   GNU General Public License for more details.
//
//   You should have received a copy of the GNU General Public License
//   along with Dartboard.  If not, see <http://www.gnu.org/licenses/>.

const int  debounceTime = 100; //  20 works better than great !

byte colPins[] = {12, 11, 10,  9,  8,  7, 6, 5};
byte rowPins[] = {A0, A1, A2, A3, A4, A5, 3, 4};

byte numCols = sizeof (colPins);
byte numRows = sizeof (rowPins);

// -------------------------------------
void setup ()
{
  Serial.begin (9600);

  for (int column = 0; column < numCols; column++)
  {
    pinMode      (colPins[column], OUTPUT);
    digitalWrite (colPins[column], HIGH);
  }

  for (int row = 0; row < numRows; row++)
  {
    pinMode      (rowPins[row], INPUT);
    digitalWrite (rowPins[row], HIGH);
  }

  pinMode (LED_BUILTIN, OUTPUT);

  Serial.print ("Dartboard ");
  Serial.print (sizeof (colPins));
  Serial.print ("X");
  Serial.print (sizeof (rowPins));
  Serial.println (" OK");
}

// -------------------------------------
void loop ()
{
  char key = getKey ();

  if (key != 0)
  {
    Serial.println (key);
  }
}

// -------------------------------------
char getKey ()
{
  char key = 0;

  for (int column = 0; column < numCols; column++)
  {
    digitalWrite (colPins[column], LOW);

    for (int row = 0; row < numRows; row++)
    {
      if (digitalRead (rowPins[row]) == LOW)
      {
        delay (debounceTime);

        while (digitalRead (rowPins[row]) == LOW)
        {
          //wait for key to be released
        }
        Serial.print (row);
        Serial.print (".");
        Serial.println (column);
      }
    }

    digitalWrite (colPins[column], HIGH);
  }

  return key;
}

// -------------------------------------
void blink ()
{
  for (int i = 0; i < 5; i++)
  {
    digitalWrite (LED_BUILTIN, HIGH);
    delay (50);

    digitalWrite (LED_BUILTIN, LOW);
    delay (50);
  }
}

