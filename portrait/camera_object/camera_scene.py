# %%
from shapely import Point, Polygon
from enum import Enum
from cv2 import aruco
import time
import cv2
import numpy as np
from shapely import Polygon, Point
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import shared_memory

from camera_object.camera_object import CameraObject, ObjectCategory
from camera_object.registry import objectRegistry, __ObjectRegistry__


def point_to_pos(p: Point):
    pos = p.coords[0]
    return (int(pos[0]), int(pos[1]))


def coords_to_pos(coords):
    return [(int(pos[0]), int(pos[1])) for pos in coords]


sift = cv2.SIFT_create()
FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
search_params = dict(checks=50)
MIN_MATCH_COUNT = 10
flann = cv2.FlannBasedMatcher(index_params, search_params)


def compute_sift_position(id, tracker_path, frame_width, frame_height):
    print("Starting SIFT for", id)
    tracker = cv2.imread(tracker_path, cv2.IMREAD_GRAYSCALE)

    tracker_kp, tracker_des = sift.detectAndCompute(tracker, None)

    shm_frame = shared_memory.SharedMemory(name="frame-buffer")
    frame = np.ndarray((frame_width, frame_height),
                       dtype=np.uint8, buffer=shm_frame.buf)

    shm_pos = shared_memory.SharedMemory(name=id+"-position")
    pos = np.ndarray((2,), dtype=np.float32, buffer=shm_pos.buf)

    h, w = tracker.shape

    while True:
        try:
            frame_copy = frame.copy()

            im_kp, im_des = sift.detectAndCompute(frame_copy, None)
            matches = flann.knnMatch(im_des, tracker_des, k=2)
            good = []
            for m, n in matches:
                if m.distance < 0.8*n.distance:
                    good.append(m)
            if len(good) > MIN_MATCH_COUNT:
                dst_pts = np.float32(
                    [im_kp[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
                src_pts = np.float32(
                    [tracker_kp[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
                M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

                pts = np.float32(
                    [[0, 0], [0, h-1], [w-1, h-1], [w-1, 0]]).reshape(-1, 1, 2)
                dst = cv2.perspectiveTransform(pts, M)
                detected_pos = np.mean(dst, axis=0).reshape(2)
                pos[:] = detected_pos[:]
                # pos[0] =
                # pos[1] = 123
                # print(id, pos)
        except Exception as e:
            # print(e)
            time.sleep(1)
        # return None


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
        self.frame = np.zeros([1, 1])

    @staticmethod
    def convert_frame(frame):
        w, h, _ = frame.shape
        ratio = 0.001
        crop_w = round(ratio*w)
        crop_h = round(ratio*h)
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        # gray_2 = gray[crop_w:(w-crop_w), crop_h:(h-crop_h)].copy()
        return gray

    def start_camera_service(self):

        while True:
            try:

                cap = cv2.VideoCapture("udp://@0.0.0.0:1234")

                ret, cam_frame = cap.read()

                converted_frame = self.convert_frame(cam_frame)
                w, h = converted_frame.shape
                print("setting width and height", w,h)
                print(objectRegistry.get_all())
                for obj in objectRegistry.get_all():
                    print("setting dims", obj.get_id(), w,h)
                    obj.width = w
                    obj.height = h
                
                # frame = np.ndarray(
                #     converted_frame.shape, dtype=converted_frame.dtype, buffer=self.shm_frame.buf)

                while True:
                    ret, cam_frame = cap.read()
                    converted_frame = self.convert_frame(cam_frame)
                    self.frame = converted_frame

                    self.update_objects_aruco(converted_frame)
                    self.draw_state()

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
            except Exception as e:
                print("error", e)
            finally:
                cap.release()

    def start_sift_processes(self):
        pass

    def start_detection_service(self):
        # pass
        print("waitig for frame")
        while self.frame.shape[0] == 1:
            time.sleep(0.5)
        print("got frame")

        # processes = []
        # for obj in objectRegistry.get_all():
        #     p = ProcessPoolExecutor().submit(
        #         compute_sift_position, obj.object_id, obj.sift_tracker_paths[0], self.frame.shape[0], self.frame.shape[1])
        #     processes.append(p)
        while True:
            self.update_objects_aruco(self.frame)
            self.draw_state()
            time.sleep(0.05)
        # while self.frame.shape[0] == 1:
        #     time.sleep(0.5)

        # while True:
        #     time.sleep(0.5)
        #     self.update_objects_aruco(self.frame)
        #     # for obj in objectRegistry.get_all():
        #     # frame = self.frame.copy()
        #     # kp, des = sift.detectAndCompute(frame, None)
        #     # obj.get_position_sift(kp, des)
        #     # obj.update_position_from_shared()
        #     # kp, des = sift.detectAndCompute(frame, None)

        #     self.draw_state()

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

    def draw_state(self):
        im = self.frame.copy()
        im = cv2.cvtColor(im, cv2.COLOR_GRAY2RGB)
        # im = cv2.drawContours(im, coords_to_pos(list(self.area_polygon.exterior.coords)), -1, (255,0,0), -1)
        for obj in objectRegistry.get_all():
            col = None
            pos = point_to_pos(obj.position_sh)
            if obj.in_bounds:
                col = (0, 0, 255)
            else:
                col = (255, 0, 0)
            im = cv2.circle(im, pos, 1, col, 30)
            # cv2.imshow("frame", im)

        self.status_frame = im

    def __del__(self):
        # cv2.destroyWindow('frame')
        # self.shm_frame.close()
        # self.shm_frame.unlink()
        pass

    def init_fixed_camera_objects(self):
        objectRegistry.add(
            CameraObject("tracker-8",category=ObjectCategory.NATURE,
                         sift_tracker_paths=[
                             'portrait/trackers/1.png'],
                         tracker_id=8

                         ),
            CameraObject("tracker-3",
                         category=ObjectCategory.NATURE,
                         sift_tracker_paths=[
                             'portrait/trackers/2.png'],
                         tracker_id=3
                         ),
            CameraObject("tracker-2",
                         category=ObjectCategory.NATURE,
                         sift_tracker_paths=[
                             'portrait/trackers/3.png'],
                         tracker_id=2
                         ),
            CameraObject("tracker-10",
                         category=ObjectCategory.NATURE,
                         sift_tracker_paths=[
                             'portrait/trackers/4.png'],
                         tracker_id=10
                         ),
            CameraObject("tracker-17",
                         category=ObjectCategory.NATURE,
                         sift_tracker_paths=[
                             'portrait/trackers/5.png'],
                         tracker_id=17
                         ),
            CameraObject("tracker-0",
                         category=ObjectCategory.NATURE,
                         sift_tracker_paths=[
                             'portrait/trackers/6.png'],
                         tracker_id=0
                         ),
            CameraObject("tracker-5",
                         category=ObjectCategory.NATURE,
                         sift_tracker_paths=[
                             'portrait/trackers/7.png'],
                         tracker_id=5
                         ),
            CameraObject("tracker-11",
                         category=ObjectCategory.NATURE,
                         sift_tracker_paths=[
                             'portrait/trackers/7.png'],
                         tracker_id=11
                         ),
            CameraObject("tracker-1",
                         category=ObjectCategory.NATURE,
                         sift_tracker_paths=[
                             'portrait/trackers/7.png'],
                         tracker_id=1
                         ),
            CameraObject("tracker-15",
                         category=ObjectCategory.NATURE,
                         sift_tracker_paths=[
                             'portrait/trackers/7.png'],
                         tracker_id=15
                         ),
            CameraObject("tracker-12",
                         category=ObjectCategory.NATURE,
                         sift_tracker_paths=[
                             'portrait/trackers/7.png'],
                         tracker_id=12
                         ),
            CameraObject("tracker-6",
                         category=ObjectCategory.NATURE,
                         sift_tracker_paths=[
                             'portrait/trackers/7.png'],
                         tracker_id=6
                         )
                         )
            #print("created", len(objectRegistry.get_all()),"objects")
            # CameraObject("testing-8", 17,
            #              category=ObjectCategory.NATURE,
            #              sift_tracker_paths=[
            #                  'portrait/trackers/11.png'],
            #              area_polygon=self.area_polygon),
            # CameraObject("testing-9", 17,
            #              category=ObjectCategory.NATURE,
            #              sift_tracker_paths=[
            #                  'portrait/trackers/11.png'],
            #              area_polygon=self.area_polygon)
        
