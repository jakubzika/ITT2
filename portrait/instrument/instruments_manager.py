import asyncio
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
                midi_out_angle=80,
                midi_out_proximity=80,
                point=Point(650, 650)
            ),
            ProximityInstrument(
                instrument_id="proximity-2",
                camera_object_id="testing-2",
                midi_out_angle=73,
                midi_out_proximity=73,
                point=Point(650, 650)
            )
        )

    async def start_service(self):
        assert self.midi_out != None
        while True:
            await asyncio.sleep(0.1)
            for instrument in instrumentRegistry.get_all():
                instrument.update()
            data = self.gather_data()
            self.send_data()

    def set_out(self, midi_out: Midi):
        self.midi_out = midi_out
