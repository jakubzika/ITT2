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
                instrument_id="proximity-1",
                camera_object_id="testing-1",
                midi_out_angle=70,
                midi_out_proximity=70,
                point=Point(1315, 800)
            ),
            ProximityInstrument(
                instrument_id="proximity-2",
                camera_object_id="testing-2",
                midi_out_angle=71,
                midi_out_proximity=71,
                point=Point(1538, 1014)
            ),
            ProximityInstrument(
                instrument_id="proximity-3",
                camera_object_id="testing-3",
                midi_out_angle=72,
                midi_out_proximity=72,
                point=Point(648, 458)
            ),
            ProximityInstrument(
                instrument_id="proximity-4",
                camera_object_id="testing-4",
                midi_out_angle=73,
                midi_out_proximity=73,
                point=Point(9773, 1112)
            ),
            ProximityInstrument(
                instrument_id="proximity-5",
                camera_object_id="testing-5",
                midi_out_angle=74,
                midi_out_proximity=74,
                point=Point(968, 1660)
            ),
            ProximityInstrument(
                instrument_id="proximity-6",
                camera_object_id="testing-6",
                midi_out_angle=75,
                midi_out_proximity=75,
                point=Point(463, 845)
            ),
            ProximityInstrument(
                instrument_id="proximity-7",
                camera_object_id="testing-7",
                midi_out_angle=76,
                midi_out_proximity=76,
                point=Point(875, 819)
            ),
            ProximityInstrument(
                instrument_id="proximity-8",
                camera_object_id="testing-8",
                midi_out_angle=77,
                midi_out_proximity=77,
                point=Point(517, 1104)
            ),
            ProximityInstrument(
                instrument_id="proximity-9",
                camera_object_id="testing-9",
                midi_out_angle=78,
                midi_out_proximity=78,
                point=Point(1167, 562)
            ),
            ProximityInstrument(
                instrument_id="proximity-10",
                camera_object_id="testing-10",
                midi_out_angle=79,
                midi_out_proximity=79,
                point=Point(1790, 900)
            ),
            ProximityInstrument(
                instrument_id="proximity-11",
                camera_object_id="testing-11",
                midi_out_angle=80,
                midi_out_proximity=80,
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
