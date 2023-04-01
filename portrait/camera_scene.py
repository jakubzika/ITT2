#%%
from cv2 import aruco
import cv2
import asyncio
import asyncio
import numpy as np

from camera_object import CameraObject
from object_registry import objectRegistry, __ObjectRegistry__

#%%

class CameraScene:
    
    objects: list[CameraObject] = []

    aruco_dict = None
    aruco_parameters = None

    def __init__(self):
        self.aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
        self.aruco_parameters = aruco.DetectorParameters_create()
    
    async def start_service(self):
        cap = cv2.VideoCapture(0)

        while True:
            await asyncio.sleep(0.3)

            ret, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            corners, ids, rejected_img_points = aruco.detectMarkers(
                gray, self.aruco_dict, parameters=self.aruco_parameters
                )
            
            self.update_objects(ids, corners)
            
    def update_objects(self, detected_ids: np.ndarray, detected_corners: np.ndarray):
        if detected_ids is None:
              detected_ids = np.array([])
              detected_corners = np.array([])

        for camera_object in objectRegistry.get_all_camera_objects():
            found = False
            object_tracker_id = camera_object.get_tracker_id()
            
            for i in range(detected_ids.shape[0]):
                tracker_id = detected_ids[i][0]
                corners = detected_corners[i]
                if tracker_id == object_tracker_id:
                    camera_object.update_position(corners[0])
                    found = True
                    break

            if not found:
                camera_object.update_position(corners=None, visible=False)

