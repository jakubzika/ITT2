import asyncio
from shapely import Point
import rerun as rr

# from instruments.ratio_instrument import RatioInstrument
# from instruments.count_instrument import CountInstrument
# from instruments.proximity_instrument import ProximityInstrument
from .instruments.presence_instrument import PresenceInstrument
from .instruments.proximity_instrument import ProximityInstrument
from .instruments.distance_sensor_instrument import DistanceSensorInstrument

from .registry import instrumentRegistry
from midi.midi import Midi


class InstrumentsManager:


    def __init__(self):
        self.instrument_data = []
        self.midi_out = None

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

    def log_data(self):
        text_log = ""
        
        for midi_port, value in self.instrument_data:
            text_log += f"port:{midi_port} val:{value}\n"

        try:
            rr.log(f"midi/{midi_port}", rr.BarChart([i[1] for i in [(0,127)] + self.instrument_data]), static=True)
            rr.log("text", rr.TextDocument(text_log), static=True)
        except Exception as e:
            pass


    def send_data(self):
        try:
            self.log_data()
        except:
            pass
        self.midi_out.send_bulk_control(self.instrument_data)

    def init_instruments(self):
        instrumentRegistry.add(
            # ProximityInstrument(
            #     instrument_id="proximity-1",
            #     camera_object_id="obj-1",
            #     midi_out_proximity=110,
            #     point=Point(764, 369)
            # ),
            # ProximityInstrument(
            #     instrument_id="proximity-1",
            #     camera_object_id="obj-1",
            #     midi_out_proximity=115,
            #     point=Point(764, 369)
            # ),
        )
        for i in range(6):
            instrumentRegistry.add(
                DistanceSensorInstrument(
                    instrument_id=f'distance-{i}',
                    sensor_id=f'Dist{i}',
                    midi_out=80 + i,
                )
            )

        for i in range(12):
            instrumentRegistry.add(
                PresenceInstrument(
                    instrument_id=f"stone-{i}",
                    midi_out=90 + i,
                    object_id=f'obj-{i}',
                ),
            )

    async def start_service(self):
        print("starting InstrumentsManager")
        assert self.midi_out != None

        try:
            while True:
                await asyncio.sleep(0.05)
                for instrument in instrumentRegistry.get_all():
                    instrument.update()
                data = self.gather_data()
                self.send_data()
        except Exception as e:
            print(e)

    def set_out(self, midi_out: Midi):
        self.midi_out = midi_out
