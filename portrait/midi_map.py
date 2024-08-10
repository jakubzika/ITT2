#%%
from midi.midi import Midi
midi_controller = Midi(port=None)

#%%

midi_controller.send_control(110, 0)

# midiout.send_message([CONTROL_CHANGE | channel , controller_number, 0x12])
