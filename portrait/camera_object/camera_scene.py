# %%
from shapely import Point, Polygon
from cv2 import aruco
import cv2
import asyncio
import asyncio
import numpy as np
from shapely import Polygon, Point
from typing import Optional
import functools
import rerun as rr
from util import shapely_polygon_to_points_list


from camera_object.camera_object import CameraObject
from camera_object.registry import objectRegistry, __ObjectRegistry__

def point_to_pos(p: Point):
    pos = p.coords[0]
    return (int(pos[0]), int(pos[1]))


def coords_to_pos(coords):
    return [(int(pos[0]), int(pos[1])) for pos in coords]


DEFAULT_POLYGON = Polygon([(740, 526), (780, 1073), (1670, 1000), (1614, 449)])

class CameraScene:
    def __init__(self, area_polygon: Polygon = DEFAULT_POLYGON):
        self.aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
        self.aruco_parameters = aruco.DetectorParameters_create()

        self.area_polygon = area_polygon

        self.init_fixed_camera_objects()

        frame = np.zeros((100, 100))
        status_frame = np.zeros((100, 100))


    def log_objects(self):
        print("CameraScene registered objects:")
        for camera_object in objectRegistry.get_all():
            print(camera_object.get_id(), camera_object.get_tracker_id())
        print("")

    async def start_service(self):
        print("starting CameraScene")
        cap = cv2.VideoCapture(1)
        
        

        while cap.isOpened():
            await asyncio.sleep(0.05)

            ret, frame = cap.read()
            # frame = np.rot90(frame, 1)
            gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            corners, ids, rejected_img_points = aruco.detectMarkers(
                gray, self.aruco_dict, parameters=self.aruco_parameters
            )

            self.update_objects(ids, corners)
            self.frame = frame
            self.log_state()
        print('video service has quit')

    def update_objects(self, detected_ids: Optional[np.ndarray], detected_corners: Optional[np.ndarray]):
        if detected_ids is None:
            detected_ids = np.array([])
            detected_corners = np.array([])
        for camera_object in objectRegistry.get_all():
            aruco_idx = next(
                (idx for idx in range(len(detected_ids)) if detected_ids[idx] == camera_object.get_tracker_id()),
                None
            )
            
            if aruco_idx != None:
                corners = detected_corners[aruco_idx]
                camera_object.update_position(corners[0])
            else:
                camera_object.update_position(corners=None, visible=False)

    def log_state(self):
        corrected_frame = np.array(self.frame)
        corrected_frame[:,:,0] = self.frame[:,:,2]
        corrected_frame[:,:,1] = self.frame[:,:,1]
        corrected_frame[:,:,2] = self.frame[:,:,0]

        rr.log("image", rr.Image(corrected_frame), static=True)

        objs = objectRegistry.get_all()
        rr.log("image", rr.Points2D(
            [i.position for i in objs], 
            colors=[(255,0,0) if i.in_bounds else (0,255,0) for i in objs],
            radii=[5 for i in objs]
        ), static=True)

        # log bounds
        rr.log("image/bounds", 
               rr.LineStrips2D(shapely_polygon_to_points_list(self.area_polygon)),
               static=True
               )
    
    def init_fixed_camera_objects(self):
        # for i in range(16):
        # obj = 
        objectRegistry.add(
            CameraObject(f"obj-0", tracker_id=7, area_polygon=self.area_polygon),
            CameraObject(f"obj-1", tracker_id=17, area_polygon=self.area_polygon),
            CameraObject(f"obj-2", tracker_id=5, area_polygon=self.area_polygon),
            CameraObject(f"obj-3", tracker_id=0, area_polygon=self.area_polygon),
            CameraObject(f"obj-4", tracker_id=10, area_polygon=self.area_polygon),
            CameraObject(f"obj-5", tracker_id=15, area_polygon=self.area_polygon),
            CameraObject(f"obj-6", tracker_id=3, area_polygon=self.area_polygon),
            CameraObject(f"obj-7", tracker_id=12, area_polygon=self.area_polygon),
            CameraObject(f"obj-8", tracker_id=11, area_polygon=self.area_polygon),
            CameraObject(f"obj-9", tracker_id=6, area_polygon=self.area_polygon),
            CameraObject(f"obj-10", tracker_id=16, area_polygon=self.area_polygon),
            CameraObject(f"obj-11", tracker_id=8, area_polygon=self.area_polygon),
            
            )

# %%

p = Polygon([(0, 0), (0, 100), (100, 100), (100, 0)])
coords_to_pos(list(p.exterior.coords))
