#%%
from enum import Enum
import numpy as np
from typing import Optional

#%%

class ObjectCategory(Enum):
    NATURE = 'nature'
    CITY = 'city'

class ObjectType(Enum):
    NORMAL = 'normal'
    
class CameraObject():
    tracker_id: int = -1
    category: ObjectCategory = None
    object_type: ObjectType = None
    visible = False
    position: np.ndarray = np.zeros(2)

    object_id: str = "unknown"

    def __init__(self,
                 object_id: str,
                 tracker_id: int,
                 category: ObjectCategory,
                 object_type: ObjectType = ObjectType.NORMAL
                 ):
        self.object_id = object_id

        self.tracker_id = tracker_id
        self.category = category
        self.object_type = object_type

    def update_position(self, corners: Optional[np.ndarray] = None, visible: bool = True):
        if not visible: 
            self.visible = False
            self.position = np.array([-1, -1])
        else:
            assert corners is not None
            if corners.shape == (2,):
                self.position = corners
            else:
                pos = np.mean(corners,axis=0)
                self.visible = True
                self.position = pos

    def get_id(self):
        return self.object_id
    
    def get_tracker_id(self):
        return self.tracker_id
    
    def id_from_detector(id):
        return "camera-object-{id}"
