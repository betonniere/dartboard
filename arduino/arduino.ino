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

byte colPins[] = {3, 4, 5, 6, 7, 8, 9, 10, 11, 12};
byte rowPins[] = {A0, A1, A2, A3};

int numCols = sizeof (colPins);
int numRows = sizeof (rowPins);

#define RED     "\033[1;31m"
#define GREEN   "\033[1;32m"
#define YELLOW  "\033[1;33m"
#define BLUE    "\033[1;34m"
#define MAGENTA "\033[1;35m"
#define CYAN    "\033[1;36m"
#define WHITE   "\033[0m"

// -------------------------------------
void setup ()
{
   Serial.begin (115200);

   // Welcome blink
   pinMode (LED_BUILTIN, OUTPUT);

   for (int i = 0; i < 3; i++)
   {
      delay (1000);
      for (int j = 0; j < 3; j++)
      {
         digitalWrite (LED_BUILTIN, HIGH);
         delay (100);
         digitalWrite (LED_BUILTIN, LOW);
         delay (100);
      }
   }

   // PIN configuration
   for (int c = 0; c < numCols; c++)
   {
      pinMode      (colPins[c], OUTPUT);
      digitalWrite (colPins[c], HIGH);
   }

   for (int r = 0; r < numRows; r++)
   {
      pinMode      (rowPins[r], INPUT);
      digitalWrite (rowPins[r], HIGH);
   }

   Serial.println (GREEN "Dartboard OK!" WHITE);
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

   for (int c = 0; c < numCols; c++)
   {
      digitalWrite (colPins[c], LOW);

      for (int r = 0; r < numRows; r++)
      {
         if (digitalRead (rowPins[r]) == LOW)
         {
            delay (debounceTime);

            while (digitalRead (rowPins[r]) == LOW)
            {
               // Wait for key to be released
            }
            Serial.print (rowPins[r]);
            Serial.print (".");
            Serial.println (colPins[c]);
         }
      }

      digitalWrite (colPins[c], HIGH);
   }

   return key;
}

// -------------------------------------
void blink ()
{
   digitalWrite (LED_BUILTIN, HIGH);
   delay (1000);

   digitalWrite (LED_BUILTIN, LOW);
   delay (1000);
}
