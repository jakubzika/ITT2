from rtmidi.midiutil import open_midioutput
from rtmidi.midiconstants import NOTE_OFF, NOTE_ON, CONTROL_CHANGE
import rtmidi
from rtmidi import midiutil
import os


class Midi:
    midi = None
    port_name = None

    def __init__(self):
        midiout = rtmidi.MidiOut()

        if os.name == 'nt':
            available_ports = midiout.get_ports()
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

        self.midi = midiout

    def send_control(self, channel, value):
        self.midi.send_message([CONTROL_CHANGE, channel, value])

    def send_bulk_control(self, values: list[tuple[int, int]]):
        for channel, value in values:
            self.send_control(channel, value)

    def get_out(self, channel: int):
        return lambda value: self.send_control(channel, value)
