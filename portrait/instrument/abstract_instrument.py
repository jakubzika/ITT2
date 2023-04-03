from abc import ABC, abstractmethod

class AbstractInstrument(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def update(self):
        print('ha')
    
    @abstractmethod
    def get_data(self):
        pass  

    @abstractmethod
    def get_id(self):
        pass
