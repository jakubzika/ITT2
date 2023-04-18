import math

from instrument.abstract_instrument import AbstractInstrument
from camera_object.registry import objectRegistry
from camera_object.camera_object import ObjectCategory


class RatioInstrument(AbstractInstrument):

    ratio = 0
    midi_out = -1

    def __init__(self, instrument_id: str, midi_out: int = -1):
        self.midi_out = midi_out
        super().__init__(instrument_id)

    def update(self):
        num_nature_objects = 0
        num_city_objects = 0

        for obj in objectRegistry.get_all():
            if obj.category is ObjectCategory.CITY:
                num_city_objects += 1
            elif obj.category is ObjectCategory.NATURE:
                num_nature_objects += 1

        max_category = ObjectCategory.CITY if num_city_objects >= num_nature_objects else ObjectCategory.NATURE
        max_val = max(num_city_objects, num_nature_objects)

        sharpness = 1
        softmax_sum = math.exp(sharpness * num_nature_objects) + \
            math.exp(sharpness * num_city_objects)
        softmax = math.exp(sharpness * num_nature_objects) / softmax_sum

        self.ratio = softmax

        return super().update()

    def get_data(self):
        return (self.midi_out, round(self.ratio, 2))
