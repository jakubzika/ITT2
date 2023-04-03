import asyncio
import json
import random
from quart import websocket, Quart
from object_registry import objectRegistry
from camera_scene import CameraScene
import base64
import cv2


def start_dashboard_stream_server(camera_scene: CameraScene):
  loop = asyncio.get_event_loop()
  app = Quart(__name__)

  @app.websocket("/objects")
  async def objects_wss_x():
    while True:
        obj = objectRegistry.get_camera_object("testing-1")
        # output = json.dumps([float(obj.position[0]),float(obj.position[1])])
        output = json.dumps([obj.prev_positions[:,0].tolist(), obj.prev_positions[:,1].tolist()])
        await websocket.send(output)
        await asyncio.sleep(0.1)

  @app.websocket("/camera")
  async def stream_video():
    while True:
        await asyncio.sleep(0.1)
        # frame = cv2.resize(camera_scene.frame, (200,200))
        frame = camera_scene.status_frame
        _, jpeg = cv2.imencode('.jpg', frame)
        raw_img = jpeg.tobytes()
        await websocket.send(f"data:image/jpeg;base64, {base64.b64encode(raw_img).decode()}")

  @app.websocket("/instrument")
  async def stream_instrument():
    while True:
      await asyncio.sleep(0.1)
      

  app.run(port=5000, loop=loop, use_reloader=False)

