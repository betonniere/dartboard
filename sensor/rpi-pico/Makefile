.SILENT:

all: compile

cmake:
	cd build && cmake .

compile:
	cd build && make -j3

upload: compile
	cp ./build/pico-dart.uf2 /media/yannick/RPI-RP2
	make monitor

monitor:
	arduino-cli monitor --config 115200 --port /dev/ttyACM0