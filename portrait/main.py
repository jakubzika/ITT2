import cv2
import asyncio
import threading
import numpy as np

from camera_object.camera_scene import CameraScene
from camera_object.registry import objectRegistry
from dashboard.stream import start_dashboard_stream_server
from dashboard.frontend import start_dashboard
from instrument.instruments_manager import InstrumentsManager
from midi.midi import Midi

DASHBOARD = True

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
        camera_scene = self.camera_scene
        # start all the async services
        camera_capture_thread = threading.Thread(target=lambda x: camera_scene.start_camera_service(), args=(1,))
        camera_capture_thread.start()
        camera_scene_thread = threading.Thread(target=lambda x: camera_scene.start_service(), args=(1,))
        camera_scene_thread.start()

        #loop.create_task(self.camera_scene.start_service())
        loop.create_task(self.instrument_manager.start_service())

        if DASHBOARD:
            dashboard_thread = threading.Thread(target=start_dashboard)
            dashboard_thread.start()
            start_dashboard_stream_server(
                self.camera_scene, self.instrument_manager)

        # ---

        loop.run_forever()

    async def log_objects(self):
        while True:
            print("---")
            for object in objectRegistry.get_all():
                print(object.object_id, object.measurements)

            await asyncio.sleep(0.3)


if __name__ == '__main__':
    main = Main()
    main.start()
