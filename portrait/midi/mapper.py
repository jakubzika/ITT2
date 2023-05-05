# %%
import rtmidi
from rtmidi.midiutil import open_midioutput
    
from rtmidi.midiconstants import NOTE_OFF, NOTE_ON, CONTROL_CHANGE


midiout, port_name = open_midioutput(None)

# %%

midiout.send_message([CONTROL_CHANGE | 0, 81, 100])

#%%

import sys
print(sys.executable)