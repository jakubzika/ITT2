import serial
from rtmidi.midiutil import open_midioutput
from rtmidi.midiconstants import NOTE_OFF, NOTE_ON, CONTROL_CHANGE
import sys

MIDI_OUTPUT_PORT = 1
MIDI_CONTROLLER_NUMBER_BASE = 2

try:
    midiout, port_name = open_midioutput(MIDI_OUTPUT_PORT)
except (EOFError, KeyboardInterrupt):
    sys.exit()

serialPort = serial.Serial(port = "COM4", baudrate=9600,
                           timeout=2, stopbits=serial.STOPBITS_ONE)

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
            for dist in serialString.split(','):
                distances.append(int(dist.split(':')[1]))
            print(distances)

            # Send data over midi
            channel = MIDI_CONTROLLER_NUMBER_BASE

            for distance in distances:
                midiout.send_message([CONTROL_CHANGE | 0, channel, distance])
                channel += 1
