from __future__ import print_function

import logging
import sys
import time

from rtmidi.midiutil import open_midioutput
from rtmidi.midiconstants import NOTE_OFF, NOTE_ON, CONTROL_CHANGE

if len(sys.argv) > 1 and sys.argv[1] == '--help':
    print("Usage: python3 {} [midi_port camera_object_count sensor_object_count]".format(sys.argv[0]))
    exit()

CAMERA_OBJECT_COUNT = 11
SENSOR_OBJECT_COUNT = 6

def map_midi_control(controller_number, controller_name, channel = 0):
    print("Next one to map is {}. Press enter when ready.".format(controller_name))
    input()
    midiout.send_message([CONTROL_CHANGE | channel , controller_number, 0x12])
    return

port = sys.argv[1] if len(sys.argv) > 1 else None

if len(sys.argv) > 3:
    CAMERA_OBJECT_COUNT = sys.argv[2]
    SENSOR_OBJECT_COUNT = sys.argv[3]

try:
    midiout, port_name = open_midioutput(port)
except (EOFError, KeyboardInterrupt):
    sys.exit()

with midiout:
    map_midi_control(1, "City vs. nature")

    i = 1

    for controller_number in range(2, CAMERA_OBJECT_COUNT + 2):
        map_midi_control(controller_number, "Camera object {}".format(i))
        i += 1

    i = 1

    for controller_number in range(CAMERA_OBJECT_COUNT + 2, SENSOR_OBJECT_COUNT + CAMERA_OBJECT_COUNT + 2):
        map_midi_control(controller_number, "Sensor object {}".format(i))
        i += 1

    print("Now exit any mapping, the channel will be flooded. Press enter when ready.")
    input()
del midiout