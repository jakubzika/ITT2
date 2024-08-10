import cv2
import asyncio
import threading
import numpy as np
import rerun as rr

from camera_object.camera_scene import CameraScene
from camera_object.registry import objectRegistry
from instrument.instruments_manager import InstrumentsManager
from midi.midi import Midi
from rerun_dashboard.blueprint import get_dashboard_blueprint

RERUN_DASHBOARD = True

# Handle everything
class Main:
    camera_scene = None

    def __init__(self):
        self.camera_scene = CameraScene()
        self.instrument_manager = InstrumentsManager()
        self.midi_out = Midi(None)

        self.instrument_manager.set_out(self.midi_out)

    def start(self):
        loop = asyncio.get_event_loop()

        # start all the async services
        loop.create_task(self.camera_scene.start_service())
        loop.create_task(self.instrument_manager.start_service())
        if RERUN_DASHBOARD:

            rr.init("ruka-z-krajiny", spawn=True)
            rr.send_blueprint(get_dashboard_blueprint())

        print("started")
        # ---

        loop.run_forever()

    async def log_objects(self):
        while True:
            print("---")
            for object in objectRegistry.get_all():
                print(object.object_id, object.prev_positions)

            await asyncio.sleep(0.3)


if __name__ == '__main__':
    main = Main()
    main.start()
