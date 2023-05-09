# %%
import sys
import rtmidi
from rtmidi.midiutil import open_midioutput

from rtmidi.midiconstants import NOTE_OFF, NOTE_ON, CONTROL_CHANGE


midiout, port_name = open_midioutput(None, use_virtual=True)

# %%

midiout.send_message([CONTROL_CHANGE | 0, 113, 113])

# %%
