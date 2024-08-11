import math

from .abstract_instrument import AbstractInstrument
from camera_object.registry import objectRegistry
from camera_object.entity import ObjectCategory


class PresenceInstrument(AbstractInstrument):
    def __init__(self, object_id:str, instrument_id: str, midi_out: int = -1):
        self.instrument_id = instrument_id
        self.object_id = object_id
        self.midi_out = midi_out

    def update(self):
        pass

    def get_data(self):
        camera_object = objectRegistry.get(self.object_id)
        return (self.midi_out, 127 if camera_object.in_bounds else 0)
    

