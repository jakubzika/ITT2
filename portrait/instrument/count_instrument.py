import math

from instrument.abstract_instrument import AbstractInstrument
from camera_object.registry import objectRegistry
from camera_object.camera_object import ObjectCategory


class CountInstrument(AbstractInstrument):

    ratio = 0
    present_objects_ratio = 0
    midi_out = -1

    def __init__(self, instrument_id: str, midi_out: int = -1):
        self.instrument_id = instrument_id
        self.midi_out = midi_out
        super().__init__(instrument_id)

    def update(self):
        camera_objects = objectRegistry.get_all()
        total_objects = len(camera_objects)
        present_objects = 0
        for obj in camera_objects:
            if obj.in_bounds:
                present_objects += 1

        self.present_objects_ratio = present_objects / total_objects

        return super().update()

    def get_data(self):
        return (self.midi_out, 255 * self.present_objects_ratio)
