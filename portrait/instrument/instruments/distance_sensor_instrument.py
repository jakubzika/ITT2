from .abstract_instrument import AbstractInstrument
from sensors.registry import sensorRegistry
from util import clip_7bit


class DistanceSensorInstrument(AbstractInstrument):
    
    def __init__(self, instrument_id:str, midi_out: int, sensor_id: str):
        self.midi_out = midi_out
        self.sensor = sensorRegistry.get(sensor_id)
        self.time = 0
        super().__init__(instrument_id)

    def update(self):
        pass

    def get_data(self):
        return [
            (self.midi_out, clip_7bit(self.sensor.reading)),
        ]