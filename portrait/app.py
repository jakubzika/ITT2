import cv2
import asyncio
import threading
import numpy as np
import rerun as rr

from camera_object.manager import CameraManager
from instrument.manager import InstrumentsManager
from sensors.manager import SensorsManager

from camera_object.registry import objectRegistry
from midi.midi import Midi
from rerun_dashboard.blueprint import get_dashboard_blueprint

RERUN_DASHBOARD = True

# Handle everything
class App:

    def __init__(self):
        self.camera_manager = CameraManager()
        self.sensors_manager = SensorsManager()
        self.instrument_manager = InstrumentsManager()

        self.midi_out = Midi()

        self.instrument_manager.set_out(self.midi_out)

    def start(self):
        loop = asyncio.get_event_loop()

        # start all the async services
        tasks = [
            ('camera_manager_task', lambda: self.camera_manager.start_service()),
            ('sensors_manager_task', lambda: self.sensors_manager.start_service()),
            ('instruments_manager_task', lambda: self.instrument_manager.start_service()),
        ]
        for task_id, task_fn in tasks:
            print("start task", task_id)
            task_handle = loop.create_task(task_fn())
            task_handle.add_done_callback(lambda x: print("quit", task_id))
            
        # [task for task in tasks]
        

        if RERUN_DASHBOARD:
            rr.init("ruka-z-krajiny", spawn=True)
            rr.send_blueprint(get_dashboard_blueprint())

        print("starting Krajinator")
        # ---

        loop.run_forever()

    async def log_objects(self):
        while True:
            print("---")
            for object in objectRegistry.get_all():
                print(object.object_id, object.prev_positions)

            await asyncio.sleep(0.3)


if __name__ == '__main__':
    main = App()
    main.start()
