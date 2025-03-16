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

#include <iostream>
#include <pico/stdlib.h>
#include <hardware/uart.h>
#include <hardware/irq.h>

#define RED     "\033[1;31m"
#define GREEN   "\033[1;32m"
#define YELLOW  "\033[1;33m"
#define BLUE    "\033[1;34m"
#define MAGENTA "\033[1;35m"
#define CYAN    "\033[1;36m"
#define WHITE   "\033[0m"

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

// ---
enum Sector
{
   LOWER = 0,
   UPPER,
   CENTER,
   RESERVED
};

// ---
struct  NumberPin
{
   int connector;
   int  value[3];
};

NumberPin number_pins[] =
{
   16, {1,  7,  0},  // Rubber A1
   17, {18, 19, 0},  // Rubber A2
   18, {4,  3,  0},  // Rubber A3
   19, {13, 17, 0},  // Rubber A4
   20, {6,  2,  0},  // Rubber A5
   21, {10, 15, 0},  // Rubber A6
   22, {20, 16, 0},  // Rubber A7
   26, {5,  8,  0},  // Rubber A8
   27, {12, 11, 25}, // Rubber A9
   28, {9, 14,  50}  // Rubber A10
};

// ---
struct RatingPin
{
   int   connector;
   Sector sector;
   int    value;
};

RatingPin rating_pins[] =
{
    0, Sector::RESERVED, 0, // Rubber B1
   15, Sector::UPPER,    3, // Rubber B2
   14, Sector::UPPER,    2, // Rubber B3
   13, Sector::UPPER,    1, // Rubber B4
   12, Sector::CENTER,   1, // Rubber B5
   11, Sector::LOWER,    1, // Rubber B6
   10, Sector::LOWER,    2, // Rubber B7
    9, Sector::LOWER,    3, // Rubber B8
    0, Sector::RESERVED, 0, // Rubber B9
    0, Sector::RESERVED, 0  // Rubber B10
};

int numbers_count = sizeof(number_pins)/sizeof(number_pins[0]);
int ratings_count = sizeof(rating_pins)/sizeof(rating_pins[0]);

// ----------------------------------------------
void setup()
{
   stdio_init_all();

   // UART
   uart_init(uart0, 115200);
   gpio_set_function(0, GPIO_FUNC_UART);

   // LED
   gpio_init(PICO_DEFAULT_LED_PIN);
   gpio_set_dir(PICO_DEFAULT_LED_PIN, GPIO_OUT);
   gpio_put(PICO_DEFAULT_LED_PIN, true);

   // OUTPUT
   for (const NumberPin& number_pin : number_pins)
   {
      if (number_pin.connector != 0)
      {
         gpio_init(number_pin.connector);
         gpio_set_dir(number_pin.connector, GPIO_OUT);

         gpio_put(number_pin.connector, false);
      }
   }

   // INPUT
   for (const RatingPin& rating_pin : rating_pins)
   {
      if (rating_pin.connector != 0)
      {
         gpio_init(rating_pin.connector);
         gpio_set_dir(rating_pin.connector, GPIO_IN);
      }
   }
}

// ----------------------------------------------
int main()
{
   const int debounceTime = 100;

   setup();

   while (true)
   {
      for (const NumberPin& number_pin : number_pins)
      {
         if (number_pin.connector != 0)
         {
            gpio_put(number_pin.connector, true);

            for (const RatingPin& rating_pin : rating_pins)
            {
               if ((rating_pin.connector != 0) && gpio_get(rating_pin.connector))
               {
                  sleep_ms (debounceTime);

                  while (gpio_get(rating_pin.connector))
                  {
                     // Wait for key to be released
                  }

                  if (number_pin.value[rating_pin.sector] == 50)
                  {
                     std::cout << "25X2" << '\n';
                  }
                  else
                  {
                     std::cout << number_pin.value[rating_pin.sector] << 'X' << rating_pin.value << '\n';
                  }
               }
            }

            gpio_put(number_pin.connector, false);
         }
      }
   }

   return 0;
}
