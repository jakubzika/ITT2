import asyncio
import time
from shapely import Point

from instrument.ratio_instrument import RatioInstrument
from instrument.count_instrument import CountInstrument
from instrument.proximity_instrument import ProximityInstrument
from instrument.registry import instrumentRegistry
from midi.midi import Midi


class InstrumentsManager:

    instrument_data = []
    midi_out = None

    def __init__(self):
        self.init_instruments()

    def gather_data(self):
        data = []
        for instrument in instrumentRegistry.get_all():
            instrument_data = instrument.get_data()

            if type(instrument_data) == list:
                data.extend(instrument_data)
            else:
                data.append(instrument_data)

        self.instrument_data = data
        return data

    def send_data(self):
        self.midi_out.send_bulk_control(self.instrument_data)

    def init_instruments(self):
        instrumentRegistry.add(
            # RatioInstrument("ratio_instrument_1", 1),
            # CountInstrument("count_instrument_2", 2),
            ProximityInstrument(
                instrument_id="pitched-2",
                camera_object_id="tracker-12",
                midi_out_angle=2,
                midi_out_proximity=2,
                point=Point(1315, 800)
            ),
            ProximityInstrument(
                instrument_id="forest-3",
                camera_object_id="tracker-8",
                midi_out_angle=3,
                midi_out_proximity=3,
                point=Point(1538, 1014)
            ),
            ProximityInstrument(
                instrument_id="smooth-sq-bass-4",
                camera_object_id="tracker-15",
                midi_out_angle=4,
                midi_out_proximity=4,
                point=Point(648, 458)
            ),
            ProximityInstrument(
                instrument_id="birds-chirping-5",
                camera_object_id="tracker-5",
                midi_out_angle=5,
                midi_out_proximity=5,
                point=Point(9773, 1112)
            ),
            ProximityInstrument(
                instrument_id="frogs-6",
                camera_object_id="tracker-6",
                midi_out_angle=6,
                midi_out_proximity=6,
                point=Point(968, 1660)
            ),
            ProximityInstrument(
                instrument_id="wind-chimes-7",
                camera_object_id="tracker-1",
                midi_out_angle=7,
                midi_out_proximity=7,
                point=Point(463, 845)
            ),
            ProximityInstrument(
                instrument_id="splashing-8",
                camera_object_id="tracker-3",
                midi_out_angle=8,
                midi_out_proximity=8,
                point=Point(875, 819)
            ),
            ProximityInstrument(
                instrument_id="cmrbrumblak-9",
                camera_object_id="tracker-17",
                midi_out_angle=9,
                midi_out_proximity=9,
                point=Point(875, 819)
            ),
            ProximityInstrument(
                instrument_id="rain-10",
                camera_object_id="tracker-2",
                midi_out_angle=10,
                midi_out_proximity=10,
                point=Point(517, 1104)
            ),
            ProximityInstrument(
                instrument_id="wind-11",
                camera_object_id="tracker-0",
                midi_out_angle=11,
                midi_out_proximity=11,
                point=Point(1167, 562)
            ),
            ProximityInstrument(
                instrument_id="sitar-12",
                camera_object_id="tracker-10",
                midi_out_angle=12,
                midi_out_proximity=12,
                point=Point(1790, 900)
            ),
            ProximityInstrument(
                instrument_id="tree-13",
                camera_object_id="tracker-11",
                midi_out_angle=113,
                midi_out_proximity=113,
                point=Point(1275, 1700)
            ),
            
        )

    def start_service(self):
        assert self.midi_out != None
        while True:
            time.sleep(0.3)
            for instrument in instrumentRegistry.get_all():
                instrument.update()
            data = self.gather_data()
            self.send_data()

    def set_out(self, midi_out: Midi):
        self.midi_out = midi_out
