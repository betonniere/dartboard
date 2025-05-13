cmake_minimum_required(VERSION 3.13)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

include($ENV{PICO_SDK_PATH}/external/pico_sdk_import.cmake)

project(pico-dart)

pico_sdk_init()

add_executable(pico-dart
   ../pico-dart.cpp
)
target_link_libraries(pico-dart pico_stdlib)
pico_enable_stdio_usb(pico-dart 1)
pico_enable_stdio_uart(pico-dart 1)
pico_add_extra_outputs(pico-dart)
