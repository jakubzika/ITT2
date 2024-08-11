from camera_object.entity import CameraEntity, ObjectCategory, ObjectType
from sensors.entity import SensorEntity

class __SensorRegistry__:
    sensors: dict[str, SensorEntity] = {}

    def __init__(self):
        pass

    def add(self, *sensors: SensorEntity):
        for sensor in sensors:
            print('adding sensors', sensor)
            self.sensors[sensor.id] = sensor

    def get(self, object_id: str):
        try:
            return self.sensors[object_id]
        except:
            raise Exception(
               f"Sensor entity with id \"{object_id}\" is not registered in SensorRegistry")

    def get_all(self):
        return self.sensors.values()


sensorRegistry = __SensorRegistry__()
