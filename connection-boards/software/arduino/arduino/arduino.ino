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

const int debounceTime = 100; //  20 works better than great !

//
//    B'    B                                                    Bull
//    9    12     5    20    15     6    13     4    18     1    Upper points
//   14    11     8    16    10     2    17     3    19     7    Lower points
//    .     .     .     .     .     .     .     .     .     .
//    .     .     .     .   ┌─.─────.┐    .     .     .     .
// ┌──.──┬──.──┬──.──┬──.──┬┴─.──┬──.┴─┬──.──┬──.──┬──.──┬──.──┐
// │  1  │  2  │  3  │  4  │  5  │  6  │  7  │  8  │  9  │ 10  │ Rubber A (Numbers)
// ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
// │  1  │  2  │  3  │  4  │  5  │  6  │  7  │  8  │  9  │ 10  │ Rubber B (Ratings)
// └─────┴──.──┴──.──┴──.──┴──.──┴──.──┴──.──┴──.──┴─────┴─────┘
//          .     .     .     .     .     .     .
//         X3    X2    X1     .    X1    X2    X3
//          Upper rating      .     Lower rating
//                          Bull
//

typedef enum
{
   LOWER = 0,
   UPPER,
   CENTER
} Sector;

// ---
typedef struct
{
   byte connector;
   int  value[3];
} NumberPin;

NumberPin number_pins[] =
{
   1  + 3, {7,  1,  0},  // Rubber A1
   2  + 3, {19, 18, 0},  // Rubber A2
   3  + 3, {3,  4,  0},  // Rubber A3
   4  + 3, {17, 13, 0},  // Rubber A4
   5  + 3, {2,  6,  0},  // Rubber A5
   6  + 3, {15, 10, 0},  // Rubber A6
   7  + 3, {16, 20, 0},  // Rubber A7
   8  + 3, {8,  5,  0},  // Rubber A8
   9  + 3, {11, 12, 25}, // Rubber A9
   10 + 3, {14, 9,  50}  // Rubber A10
};

// ---
typedef struct
{
   byte   connector;
   Sector sector;
   int    value;
} RatingPin;

RatingPin rating_pins[] =
{
   0,  0,      0, // Rubber B1
   A0, UPPER,  3, // Rubber B2
   A1, UPPER,  2, // Rubber B3
   A2, UPPER,  1, // Rubber B4
   3,  CENTER, 1, // Rubber B5
   A3, LOWER,  1, // Rubber B6
   A4, LOWER,  2, // Rubber B7
   A5, LOWER,  3, // Rubber B8
   0,  0,      0, // Rubber B9
   0,  0,      0  // Rubber B10
};

int numbers_count = sizeof(number_pins)/sizeof(number_pins[0]);
int ratings_count = sizeof(rating_pins)/sizeof(rating_pins[0]);

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

   // PIN configuration
   for (int v = 0; v < numbers_count; v++)
   {
      NumberPin *number_pin = &number_pins[v];

      if (number_pin->connector != 0)
      {
         pinMode      (number_pin->connector, OUTPUT);
         digitalWrite (number_pin->connector, HIGH);
      }
   }

   for (int r = 0; r < ratings_count; r++)
   {
      RatingPin *rating_pin = &rating_pins[r];

      if (rating_pin->connector != 0)
      {
         pinMode      (rating_pin->connector, INPUT);
         digitalWrite (rating_pin->connector, HIGH);
      }
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

   for (int v = 0; v < numbers_count; v++)
   {
      NumberPin *number_pin = &number_pins[v];

      if (number_pin->connector != 0)
      {
         digitalWrite (number_pin->connector, LOW);

         for (int r = 0; r < ratings_count; r++)
         {
            RatingPin *rating_pin = &rating_pins[r];

            if ((rating_pin->connector != 0) && (digitalRead (rating_pin->connector) == LOW))
            {
               delay (debounceTime);

               while (digitalRead (rating_pin->connector) == LOW)
               {
                  // Wait for key to be released
               }

               if (number_pin->value[rating_pin->sector] == 50)
               {
                  Serial.print (25);
                  Serial.print ("X");
                  Serial.println (2);
               }
               else
               {
                  Serial.print (number_pin->value[rating_pin->sector]);
                  Serial.print ("X");
                  Serial.println (rating_pin->value);
               }
            }
         }

         digitalWrite (number_pin->connector, HIGH);
      }
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
