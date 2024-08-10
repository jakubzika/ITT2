from enum import Enum
import numpy as np
from typing import Optional
from shapely import Point, Polygon


class ObjectCategory(Enum):
    NATURE = 'nature'
    CITY = 'city'

class ObjectType(Enum):
    NORMAL = 'normal'

class CameraObject():
    def __init__(self,
                 object_id: str,
                 tracker_id: int,
                 area_polygon: Polygon,
                 category: ObjectCategory = ObjectCategory.NATURE,
                 object_type: ObjectType = ObjectType.NORMAL,
                 ):
        self.object_id = object_id

        self.tracker_id = tracker_id
        self.category = category
        self.object_type = object_type

        self.area_polygon = area_polygon

        ## 
        self.visible = False
        self.in_bounds = False
        
        self.position: np.ndarray = np.zeros(2)
        self.position_sh: Point = Point(0, 0)
        self.prev_positions = np.zeros((150, 2))

    def update_position(self, corners: Optional[np.ndarray] = None, visible: bool = True):
        if not visible:
            self.visible = False
        else:
            assert corners is not None
            if corners.shape == (2,):
                self.position = np.array(corners)
            else:
                pos = np.mean(corners, axis=0)
                self.visible = True
                old_factor = 0.0
                self.position = old_factor*self.position + (1-old_factor)*pos
                self.position_sh = Point(self.position[0], self.position[1])

        self.prev_positions = np.roll(self.prev_positions, -1, axis=0)
        self.prev_positions[-1] = self.position

        self.update_in_bounds()

    def update_in_bounds(self):
        self.in_bounds = self.area_polygon.contains(self.position_sh)

    def get_id(self):
        return self.object_id

    def get_tracker_id(self):
        return self.tracker_id

    def id_from_detector(id):
        return "camera-object-{id}"
