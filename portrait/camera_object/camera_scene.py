# %%
from shapely import Point, Polygon
from cv2 import aruco
import cv2
import asyncio
import asyncio
import numpy as np
from shapely import Polygon, Point
import functools
from concurrent.futures import ProcessPoolExecutor


from camera_object.camera_object import CameraObject, ObjectCategory, ObjectType
from camera_object.registry import objectRegistry, __ObjectRegistry__

# %%


def point_to_pos(p: Point):
    pos = p.coords[0]
    return (int(pos[0]), int(pos[1]))


def coords_to_pos(coords):
    return [(int(pos[0]), int(pos[1])) for pos in coords]

# %%


executor = ProcessPoolExecutor(1)

DEFAULT_POLYGON = Polygon([(200, 300), (200, 1000), (600, 1000), (600, 300)])


class CameraScene:
    # aruco parameters
    aruco_dict = None
    aruco_parameters = None

    # current frame
    frame = np.zeros((100, 100))

    # frame with more data
    status_frame = np.zeros((100, 100))

    # area polygon
    area_polygon = None

    def __init__(self, area_polygon: Polygon = DEFAULT_POLYGON):
        self.aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
        self.aruco_parameters = aruco.DetectorParameters_create()

        self.area_polygon = area_polygon

        self.init_fixed_camera_objects()

    async def start_service(self):
        cap = cv2.VideoCapture(0)
        # cap = cv2.VideoCapture("udp://0.0.0.0:1234")
        # cap = cv2.VideoCapture(
        #     "/Users/jakubzika/Movies/Film 02.04.2023 v 11.30.mov")

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
            await self.draw_state()

    def update_objects(self, detected_ids: np.ndarray, detected_corners: np.ndarray):
        if detected_ids is None:
            detected_ids = np.array([])
            detected_corners = np.array([])

        for camera_object in objectRegistry.get_all():
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

    async def draw_state(self):
        im = self.frame.copy()
        # im = cv2.drawContours(im, coords_to_pos(list(self.area_polygon.exterior.coords)), -1, (255,0,0), -1)
        for obj in objectRegistry.get_all():
            col = None
            pos = point_to_pos(obj.position_sh)
            if obj.in_bounds:
                col = (0, 0, 255)
            else:
                col = (255, 0, 0)
            im = cv2.circle(im, pos, 1, col, 10)

        self.status_frame = im

    def init_fixed_camera_objects(self):
        obj1 = CameraObject("testing-1", 8, ObjectCategory.CITY,
                            area_polygon=self.area_polygon)
        obj2 = CameraObject("testing-2", 17, ObjectCategory.CITY,
                            area_polygon=self.area_polygon)
        objectRegistry.add(obj1)
        objectRegistry.add(obj2)


# %%

p = Polygon([(0, 0), (0, 100), (100, 100), (100, 0)])
coords_to_pos(list(p.exterior.coords))
