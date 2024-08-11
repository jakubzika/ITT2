#%%
from midi.midi import Midi
midi_controller = Midi()

#%%
import rtmidi
from rtmidi.midiconstants import CONTROL_CHANGE
midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()
print(available_ports)

if available_ports:
    for port in available_ports:
        if 'loopMIDI' in port:
            loopMIDI_port = int(port[-1])
            midiout.open_port(loopMIDI_port)
        else:
            loopMIDI_port = None
    if not(loopMIDI_port):
        print("loopMIDI not set up")
else:
    midiout.open_virtual_port("My virtual output")

#%%
#midiout.send_message([CONTROL_CHANGE, 110 , 50])
for i in range(80,80+6):
    if i in range(80,80):
        midi_controller.send_control(i, 126)
    else:
        midi_controller.send_control(i, 0)

#%%
for i in range(90,90+12):
    midi_controller.send_control(i, 120)