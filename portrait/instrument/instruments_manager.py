import asyncio
from shapely import Point
import rerun as rr

from instrument.ratio_instrument import RatioInstrument
from instrument.count_instrument import CountInstrument
from instrument.proximity_instrument import ProximityInstrument
from instrument.presence_instrument import PresenceInstrument

from instrument.registry import instrumentRegistry
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
        # rr.log("midi", rr.Boxes2D(
        #     [10,10],
        #     mins=[10,10],
        #     sizes=[10,10],
            
        #     labels=["aaa"]
        #     ), static=True)
        # print(self.instrument_data)
        text_log = ""
        
        # rr.log(f"midi/-1", rr.BarChart([100]), static=True)
        for midi_port, value in self.instrument_data:
            text_log += f"port:{midi_port} val:{value}\n"

        rr.log(f"midi/{midi_port}", rr.BarChart([i[1] for i in [(0,127)] + self.instrument_data]), static=True)
            

        rr.log("text", rr.TextDocument(text_log), static=True)


    def send_data(self):
        try:
            self.log_data()
        except:
            pass
        self.midi_out.send_bulk_control(self.instrument_data)

    def init_instruments(self):
        instrumentRegistry.add(
            ProximityInstrument(
                instrument_id="proximity-1",
                camera_object_id="obj-1",
                midi_out_angle=0,
                midi_out_proximity=110,
                point=Point(764, 369)
            ),
            # ProximiptyInstrument(
            #     instrument_id="proximity-2",
            #     camera_object_id="obj-2",
            #     midi_out_angle=76,
            #     midi_out_proximity=76,
            #     point=Point(100, 100)
            # ),
            # PresenceInstrument(
            #     instrument_id="stone-1",
            #     midi_out=90,
            #     object_id='obj-1',
            # )
        )

    async def start_service(self):
        print("starting InstrumentsManager")
        assert self.midi_out != None
        while True:
            await asyncio.sleep(0.05)
            for instrument in instrumentRegistry.get_all():
                instrument.update()
            data = self.gather_data()
            self.send_data()

    def set_out(self, midi_out: Midi):
        self.midi_out = midi_out
