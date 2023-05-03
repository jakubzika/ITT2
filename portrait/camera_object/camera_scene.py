# %%
from shapely import Point, Polygon
from enum import Enum
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
sift = cv2.SIFT_create()


def point_to_pos(p: Point):
    pos = p.coords[0]
    return (int(pos[0]), int(pos[1]))


def coords_to_pos(coords):
    return [(int(pos[0]), int(pos[1])) for pos in coords]

# %%


executor = ProcessPoolExecutor(1)

DEFAULT_POLYGON = Polygon([(200, 300), (200, 1000), (600, 1000), (600, 300)])


class DetectionMode(Enum):
    ARUCO = 'aruco'
    SIFT = 'sift'


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

    detection_mode = DetectionMode.ARUCO

    def __init__(self, area_polygon: Polygon = DEFAULT_POLYGON, mode: DetectionMode = DetectionMode.ARUCO):
        self.aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
        self.aruco_parameters = aruco.DetectorParameters_create()

        self.area_polygon = area_polygon

        self.init_fixed_camera_objects()

        self.detection_mode = mode

    async def start_service(self):
        # cap = cv2.VideoCapture(0)
        # cap = cv2.VideoCapture(
        #     "/Users/jakubzika/Movies/Film 02.04.2023 v 11.30.mov")
        # cap = cv2.VideoCapture(
        #     "/Users/jakubzika/School/Magistr/2.semestr/ITT2/ITT2/videos/01.mov")
        # cap.set(cv2.CV_CAP_PROP_BUFFERSIZE, 3)


        while True:
            cap = cv2.VideoCapture("udp://0.0.0.0:1234")
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            try:

                ret, frame = cap.read()

                w, h, _ = frame.shape

                for obj in objectRegistry.get_all():
                    obj.width = w
                    obj.height = h
                
                for i in range(50):
                #while cap.isOpened():
                    await asyncio.sleep(0.05)

                    for j in range(5):
                        ret, frame = cap.read()
                    ret, frame = cap.read()
                    

                    # frame = np.rot90(frame, 1)

                    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

                    w, h = gray.shape
                    # gray = cv2.resize(gray, (int(h*0.8), int(w*0.8)))

                    # try:
                    # self.update_objects_aruco(gray)
                    self.update_objects_sift(gray)

                    self.frame = frame
                    # except Exception as e:
                    #     print("failed", e)

                    await self.draw_state()
            except Exception as e:
                cap.release()
                print("err",e)

    def update_objects_aruco(self, img: np.ndarray):
        detected_corners, detected_ids, rejected_img_points = aruco.detectMarkers(
            img, self.aruco_dict, parameters=self.aruco_parameters
        )
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
                    camera_object.get_position_aruco(corners[0])
                    found = True
                    break

            if not found:
                camera_object.get_position_aruco(
                    corners=None, visible=False)

    def update_objects_sift(self, img):
        kp, des = sift.detectAndCompute(img, None)
        for camera_object in objectRegistry.get_all():
            found = camera_object.get_position_sift(kp, des)
            # print(camera_object.get_id(), found, camera_object.position_sh)

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
        obj1 = CameraObject("testing-1", 8,
                            category=ObjectCategory.NATURE,
                            sift_tracker_paths=[
                                'D:/itt/kuba/images/tracker45.png'],
                            area_polygon=self.area_polygon,

                            )
        obj2 = CameraObject("testing-2", 17,
                            category=ObjectCategory.NATURE,
                            sift_tracker_paths=[
                               'D:/itt/kuba/images/tracker46.png'],
                            area_polygon=self.area_polygon)
        objectRegistry.add(obj1)
        objectRegistry.add(obj2)


# %%
