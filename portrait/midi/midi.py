from rtmidi.midiutil import open_midioutput
from rtmidi.midiconstants import NOTE_OFF, NOTE_ON, CONTROL_CHANGE
import rtmidi
from rtmidi import midiutil


class Midi:
    midi = None
    port_name = None

    def __init__(self, port):
        midiout = rtmidi.MidiOut()

        midiout.open_virtual_port("instrumento")
        self.midi = midiout

    def send_control(self, channel, value):
        self.midi.send_message([CONTROL_CHANGE | 0, channel, value])

    def send_bulk_control(self, values: list[tuple[int, int]]):
        for channel, value in values:
            self.send_control(channel, value)

    def get_out(self, channel: int):
        return lambda value: self.send_control(channel, value)
