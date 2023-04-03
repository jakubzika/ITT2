import cv2
import asyncio
import threading
import numpy as np

from camera_scene import CameraScene
from object_registry import objectRegistry
from dashboard.stream import start_dashboard_stream_server
from dashboard.frontend import start_dashboard

DASHBOARD = True

# Handle everything
class Main:
    camera_scene = None

    def __init__(self):
      self.camera_scene = CameraScene()
    
    def start(self):
      loop = asyncio.get_event_loop()

      # start all the async services
      loop.create_task(self.camera_scene.start_service())
      
      # loop.create_task(self.log_objects())

      if DASHBOARD: 
        dashboard_thread = threading.Thread(target=start_dashboard)
        dashboard_thread.start()
        start_dashboard_stream_server(self.camera_scene)
      
      # ---

      loop.run_forever()

    async def log_objects(self):
      while True:
        print("---")
        for object in objectRegistry.get_all_camera_objects():
          print(object.object_id, object.prev_positions)
          pass

        await asyncio.sleep(0.3)

if __name__ == '__main__':
    main = Main()
    main.start()
    