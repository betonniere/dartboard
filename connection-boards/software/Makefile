.SILENT:

all: compile

monitor:
	arduino-cli monitor --config 115200 --port /dev/ttyACM0

compile:
	cd .. && arduino-cli compile --fqbn $(fqbn) $(sketch)

upload: compile
	cd .. && arduino-cli upload --fqbn $(fqbn) -p /dev/ttyACM0 $(sketch)
