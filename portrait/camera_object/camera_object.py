# %%
from enum import Enum
import numpy as np
from typing import Optional
from shapely import Point, Polygon
import os
import cv2

# %%
sift = cv2.SIFT_create()
FLANN_INDEX_KDTREE = 1
MIN_MATCH_COUNT = 20
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
search_params = dict(checks=50)
flann = cv2.FlannBasedMatcher(index_params, search_params)


weights = np.flip(np.arange(15))/5
weights = weights / np.sum(weights)
num_weights = weights.shape[0]
# weights
# %%


def get_tracker(tracker_name: str):
    project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(project_path, "trackers", tracker_name)
    return path


class ObjectCategory(Enum):
    NATURE = 'nature'
    CITY = 'city'


class ObjectType(Enum):
    NORMAL = 'normal'


class CameraObject():

    # aruco tag IDp
    # tracker_id: int = -1

    # is object visible
    # visible = False

    # is object within working area
    # in_bounds = False

    # objects position
    # position: np.ndarray = np.zeros(2)
    # position_sh: Point = Point(0, 0)

    # object_id: str = "unknown"
    # area_polygon = None

    def __init__(self,
                 object_id: str,
                 tracker_id: int,
                 sift_tracker_paths: list[str],
                 category: ObjectCategory,
                 area_polygon: Polygon,
                 object_type: ObjectType = ObjectType.NORMAL,
                 ):
        self.object_id = object_id

        self.tracker_id = tracker_id
        self.sift_tracker_paths = sift_tracker_paths

        self.category = category
        self.object_type = object_type

        self.area_polygon = area_polygon
        self.sift_trackers = []
        self.load_sift_trackers()

        self.position = np.zeros(2)
        self.position_sh = Point(0, 0)
        self.in_bounds = False

        self.tracked_position = []

        self.measurements = np.zeros((150, 2))

        self.width = 0
        self.height = 0

    def load_sift_trackers(self):
        for path in self.sift_tracker_paths:
            tracker_img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
            kp, des = sift.detectAndCompute(tracker_img, None)
            self.sift_trackers.append((tracker_img,kp, des))

    def get_position_sift(self, im_kp, im_des):

        for tracker_img, tracker_kp, tracker_des in self.sift_trackers:
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
                h, w = tracker_img.shape
                pts = np.float32(
                    [[0, 0], [0, h-1], [w-1, h-1], [w-1, 0]]).reshape(-1, 1, 2)
                dst = cv2.perspectiveTransform(pts, M)
                pos = np.mean(dst, axis=0).reshape(2)
                self.update_position(pos)
                return True

        return False

    def get_position_aruco(self, corners: Optional[np.ndarray] = None, visible: bool = True):
        if not visible:
            self.update_position(None)
        else:
            assert corners is not None
            if corners.shape == (2,):
                pos = corners
            else:
                pos = np.mean(corners, axis=0)
            self.update_position(pos)

    def update_position(self, position: np.ndarray | None):
        if position is not None:
            self.visible = True

        else:
            self.visible = False

        position = np.minimum(position, [self.width, self.height])
        position = np.maximum(position, [0, 0])
        self.position = position

        self.measurements = np.roll(self.measurements, -1, axis=0)
        self.measurements[-1] = position

        measurements_slice = self.measurements[-num_weights:].copy()
        # mult = np.multiply(measurements_slice, weights, axis=1)
        measurements_slice[:, 0] *= weights
        measurements_slice[:, 1] *= weights
        # self.position = np.sum(measurements_slice, axis=0)

        self.position_sh = Point(self.position[0], self.position[1])

        print(self.get_id(), self.position)
        self.update_in_bounds()

    def update_in_bounds(self):
        self.in_bounds = self.area_polygon.contains(self.position_sh)

    def get_id(self):
        return self.object_id

    def get_tracker_id(self):
        return self.tracker_id

    def id_from_detector(id):
        return "camera-object-{id}"
