from __future__ import print_function

import logging
import sys
import time

from rtmidi.midiutil import open_midioutput
from rtmidi.midiconstants import NOTE_OFF, NOTE_ON, CONTROL_CHANGE


log = logging.getLogger('midiout')
logging.basicConfig(level=logging.DEBUG)

# Prompts user for MIDI input port, unless a valid port number or name
# is given as the first argument on the command line.
# API backend defaults to ALSA on Linux.
port = sys.argv[1] if len(sys.argv) > 1 else None

try:
    midiout, port_name = open_midioutput(port)
except (EOFError, KeyboardInterrupt):
    sys.exit()


with midiout:
    channel = 67
    midiout.send_message([CONTROL_CHANGE | 1 , channel, 0x12])
    print("Map it now");
    time.sleep(3)
    # midiout.send_message([CONTROL_CHANGE & 0xF0, channel, 0x7f])


    # for i in range (40, 100, 2):
    #     note_on = [NOTE_ON, i, 112]  # channel 1, middle C, velocity 112
    #     note_off = [NOTE_OFF, 2, 0]
    #     print("Sending NoteOn event.")
    #     midiout.send_message(note_on)
    #     time.sleep(0.05)
    #     #print("Sending NoteOff event.")
    #     midiout.send_message(note_off)

# del midiout
print("Exit.")


