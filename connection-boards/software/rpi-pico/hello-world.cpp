#include <iostream>
#include <array>
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

#define OUTPUT_PIN 15
#define INPUT_PIN 14

void uart_init() {
    uart_init(uart0, 115200);

    gpio_set_function(0, GPIO_FUNC_UART);
    gpio_set_function(1, GPIO_FUNC_UART);
}

int main() {
   stdio_init_all();
   uart_init();

   gpio_init(PICO_DEFAULT_LED_PIN);
   gpio_set_dir(PICO_DEFAULT_LED_PIN, GPIO_OUT);

   gpio_init(OUTPUT_PIN);
   gpio_set_dir(OUTPUT_PIN, GPIO_OUT);

   gpio_init(INPUT_PIN);
   gpio_set_dir(INPUT_PIN, GPIO_IN);

   while (true) {
      std::array<bool, 2> outputs = {false, true};

      for (const bool& output : outputs) {
         bool input_value;

         gpio_put(OUTPUT_PIN, output);
         input_value = gpio_get(INPUT_PIN);
         gpio_put(PICO_DEFAULT_LED_PIN, output);

         std::cout << "==> ";
         if (input_value) {
            std::cout << GREEN;
         }
         else {
            std::cout << RED;
         }
         std::cout << std::boolalpha << input_value << WHITE << std::endl;

         sleep_ms(1000);
      }
   }

   return 0;
}
