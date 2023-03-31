#%%
from enum import Enum
import numpy as np

#%%

class ObjectCategory(Enum):
    NATURE = 'nature'
    CITY = 'city'

class ObjectType(Enum):
    NORMAL = 'normal'
    
class Object():
    tracker_id: int = -1
    category: ObjectCategory = None
    object_type: ObjectType = None
    visible = False
    cam_space_position: np.ndarray = np.zeros(2)

    def __init__(self, tracker_id: int, category: ObjectCategory, object_type: ObjectType):
        self.tracker_id = tracker_id
        self.category = category
        self.object_type = object_type

    def update_position(self, new_coords:np.ndarray = None, visible: bool = True):
        assert new_coords.shape == (2,)

        if not visible: 
            self.visible = False
            self.update_position = np.array([-1, -1])

        self.cam_space_position = new_coords

