#%%
from enum import Enum
import numpy as np
from typing import Optional
from shapely import Point, Polygon

#%%

class ObjectCategory(Enum):
    NATURE = 'nature'
    CITY = 'city'

class ObjectType(Enum):
    NORMAL = 'normal'
    
class CameraObject():

    # aruco tag ID
    tracker_id: int = -1


    category: ObjectCategory = None
    object_type: ObjectType = None

    # is object visible
    visible = False

    # is object within working area
    in_bounds = False

    # objects position
    position: np.ndarray = np.zeros(2)
    position_sh: Point = Point(0,0)
    

    prev_positions = np.zeros((150, 2))

    object_id: str = "unknown"
    area_polygon = None

    def __init__(self,
                 object_id: str,
                 tracker_id: int,
                 category: ObjectCategory,
                 area_polygon: Polygon,
                 object_type: ObjectType = ObjectType.NORMAL,
                 ):
        self.object_id = object_id

        self.tracker_id = tracker_id
        self.category = category
        self.object_type = object_type

        self.area_polygon = area_polygon

    def update_position(self, corners: Optional[np.ndarray] = None, visible: bool = True):
        if not visible: 
            self.visible = False
            #self.position = np.array([-1, -1])
        else:
            assert corners is not None
            if corners.shape == (2,):
                self.position = corners
            else:
                pos = np.mean(corners,axis=0)
                self.visible = True
                self.position = pos
                self.position_sh = Point(pos[0], pos[1])

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
