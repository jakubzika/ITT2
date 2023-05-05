# %%
from shapely import Point, Polygon
from enum import Enum
from cv2 import aruco
import time
import cv2
import asyncio
import asyncio
import numpy as np
import threading
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
        self.frame = np.zeros([1,1])

    def start_camera_service(self):
        while True:
            cap = cv2.VideoCapture("udp://@0.0.0.0:1234")
            #cap.set(cv2.CAP_PROP_BUFFERSIZE, 5)
            try:

                ret, cam_frame = cap.read()
#                while cam_frame == None:
 #                   ret, cam_frame = cap.read()


                print("read some", cam_frame)
                w, h, _ = cam_frame.shape
                crop_w = round(0.08*w)
                crop_h = round(0.08*h)

                for obj in objectRegistry.get_all():
                    obj.width = w
                    obj.height = h
                
                for i in range(50000):
                #while cap.isOpened():
                    # await asyncio.sleep(0.05)

                    # for j in range(3):
                    #     ret, frame = cap.read()
                    ret, frame = cap.read()
                    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
                    gray_2 = gray[crop_w:(w-crop_w),crop_h:(h-crop_h)].copy()
                    self.frame = gray_2

                    
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
            finally:
                cap.release()


    def start_service(self):
        # cap = cv2.VideoCapture(0)
        # cap = cv2.VideoCapture(
        #     "/Users/jakubzika/Movies/Film 02.04.2023 v 11.30.mov")
        # cap = cv2.VideoCapture(
        #     "/Users/jakubzika/School/Magistr/2.semestr/ITT2/ITT2/videos/01.mov")
        # cap.set(cv2.CV_CAP_PROP_BUFFERSIZE, 3)
        print("staring camera scene")
        while self.frame.shape[0] == 1:
            time.sleep(0.5)
        
        print("acquired frame")

        while True:
            print('sift detect')
            frame = self.frame.copy()
            self.update_objects_sift(frame)

            self.draw_state()
            

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

    def draw_state(self):
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
                               'D:/itt/kuba/images/tracker49.png'],
                            area_polygon=self.area_polygon)

        obj3 = CameraObject("testing-3", 17,
                            category=ObjectCategory.NATURE,
                            sift_tracker_paths=[
                                'D:/itt/kuba/images/tracker47.png'],
                            area_polygon=self.area_polygon)
        obj4 = CameraObject("testing-4", 17,
                            category=ObjectCategory.NATURE,
                            sift_tracker_paths=[
                                'D:/itt/kuba/images/tracker48.png'],
                            area_polygon=self.area_polygon)
        obj5 = CameraObject("testing-5", 17,
                            category=ObjectCategory.NATURE,
                            sift_tracker_paths=[
                                'D:/itt/kuba/images/tracker49.png'],
                            area_polygon=self.area_polygon)
        obj6 = CameraObject("testing-6", 17,
                            category=ObjectCategory.NATURE,
                            sift_tracker_paths=[
                                'D:/itt/kuba/images/tracker50.png'],
                            area_polygon=self.area_polygon)
        objectRegistry.add(obj1)
        objectRegistry.add(obj2)
        objectRegistry.add(obj3)
        objectRegistry.add(obj4)
        objectRegistry.add(obj5)
        objectRegistry.add(obj6)






# %%
