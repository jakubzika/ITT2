import asyncio
from camera_scene import CameraScene
from object_registry import objectRegistry

# Handle everything
class Main:
    camera_scene = None

    def __init__(self):
      self.camera_scene = CameraScene()
    
    def start(self):
      loop = asyncio.get_event_loop()

      # start all the async services
      loop.create_task(self.camera_scene.start_service())
      loop.create_task(self.log_objects())
      # ---

      loop.run_forever()

    async def log_objects(self):
      while True:
        for object in objectRegistry.get_all_camera_objects():
          # print(object.position, object.visible)
          pass

        await asyncio.sleep(0.3)

if __name__ == '__main__':
    main = Main()
    main.start()
    