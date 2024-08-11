import math
import shapely
from shapely import Point
import numpy as np

from .abstract_instrument import AbstractInstrument
from camera_object.registry import objectRegistry


class ProximityInstrument(AbstractInstrument):

    ratio = 0
    present_objects_ratio = 0
    midi_out_proximity = -1
    midi_out_angle = -1

    anchor_point = None

    camera_object = None

    angle = 0
    proximity = 0

    def __init__(self,
                 instrument_id: str,
                 camera_object_id: str,
                 midi_out_proximity: int,
                 point: Point
                 ):
        self.instrument_id = instrument_id
        self.midi_out_proximity = midi_out_proximity
        self.anchor_point = point

        self.camera_object = objectRegistry.get(camera_object_id)

        super().__init__(instrument_id)

    def update(self):
        current_pos = self.camera_object.position_sh
        anchor = self.anchor_point
        self.proximity = int(shapely.distance(current_pos, anchor) / 5)

        self.angle = np.degrees(
            np.arctan2(current_pos.x - anchor.x, current_pos.y - anchor.y)
        )

    def get_data(self):
        if not self.camera_object.in_bounds:
            return [
                (self.midi_out_proximity, 0)
            ]

        return [
            # (self.midi_out_angle, min(np.abs(self.angle), 100)),
            (self.midi_out_proximity, min(self.proximity, 127)),
        ]
