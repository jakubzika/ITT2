from camera_object.entity import CameraEntity, ObjectCategory, ObjectType
from .instruments.abstract_instrument import AbstractInstrument


class __InstrumentRegistry__:
    instruments: dict[str, AbstractInstrument] = {}

    def __init__(self):
        pass

    def add(self, *instruments: AbstractInstrument):
        for instrument in instruments:
            self.instruments[instrument.get_id()] = instrument

    def get(self, object_id: str):
        try:
            return self.instruments[object_id]
        except:
            raise Exception(
                "Instrument with id\"{id}\" is not registered in ObjectRegistry")

    def get_all(self):
        return self.instruments.values()


instrumentRegistry = __InstrumentRegistry__()
