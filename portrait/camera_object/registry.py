from camera_object.entity import CameraEntity, ObjectCategory, ObjectType


class __ObjectRegistry__:
    camera_objects: dict[str, CameraEntity] = {}
    camera_tracker_objects: dict[int, CameraEntity] = {}
    iot_objects = {}

    def __init__(self):
        pass

    def add(self, *objects: CameraEntity):
        for object in objects:
            self.camera_objects[object.get_id()] = object
            self.camera_tracker_objects[object.get_tracker_id()] = object

    def get(self, object_id: str):
        try:
            return self.camera_objects[object_id]
        except:
            raise Exception(f"Camera object with id '{object_id}' is not registered in ObjectRegistry")

    def get_all(self):
        return self.camera_objects.values()

    def get_by_tracker_id(self, tracker_id: int):
        return self.camera_tracker_objects[tracker_id]


objectRegistry = __ObjectRegistry__()
