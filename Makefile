.SILENT:

all: compile

monitor:
	arduino-cli monitor --config 115200 --port /dev/ttyACM0

compile:
	arduino-cli compile --fqbn arduino:avr:uno arduino

upload: compile
	arduino-cli upload --fqbn arduino:avr:uno -p /dev/ttyACM0 arduino
