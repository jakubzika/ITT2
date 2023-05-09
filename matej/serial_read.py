import serial
from rtmidi.midiutil import open_midioutput
from rtmidi.midiconstants import NOTE_OFF, NOTE_ON, CONTROL_CHANGE
import sys
import warnings
import serial
import serial.tools.list_ports

arduino_ports = [
    p.device
    for p in serial.tools.list_ports.comports()
    if 'Arduino' in p.description  # may need tweaking to match new arduinos
]
if not arduino_ports:
    raise IOError("No Arduino found")
if len(arduino_ports) > 1:
    warnings.warn('Multiple Arduinos found - using the first')

serialPort = serial.Serial(port = arduino_ports[0], baudrate=9600,
                           timeout=2, stopbits=serial.STOPBITS_ONE)

MIDI_OUTPUT_PORT = 1
MIDI_CONTROLLER_NUMBER_BASE = 2

try:
    midiout, port_name = open_midioutput(MIDI_OUTPUT_PORT)
except (EOFError, KeyboardInterrupt):
    sys.exit()

serialString = ""                           # Used to hold data coming over UART


with midiout:
    while(1):
        # Wait until there is data waiting in the serial buffer
        if(serialPort.in_waiting > 0):
            # Read data out of the buffer until a carraige return / new line is found
            serialString = serialPort.readline()

            # Print the contents of the serial data
            serialString = serialString.decode('Ascii')
            #print(serialString)
            distances = []

            for rawDist in serialString.split(','):
                rawDistData = rawDist.split(':')

                if len(rawDistData < 2):
                    continue                

                dist = rawDistData[1]

                if not dist.is_numeric():
                    continue

                distances.append(int(dist))
            print(distances)

            # Send data over midi
            channel = MIDI_CONTROLLER_NUMBER_BASE

            for distance in distances:
                midiout.send_message([CONTROL_CHANGE | 0, channel, distance])
                channel += 1
