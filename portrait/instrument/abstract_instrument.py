from abc import ABC, abstractmethod


class AbstractInstrument(ABC):
    instrument_id = ""

    def __init__(self, instrument_id: str):
        self.instrument_id = instrument_id

    @abstractmethod
    def update(self):
        pass

    def get_id(self):
        return self.instrument_id

    @abstractmethod
    def get_data(self) -> list[tuple[int, float | int]] | tuple[int, float | int]:
        pass

    def get_name(self):
        return f"{self.instrument_id}[{self.midi_out}]"
