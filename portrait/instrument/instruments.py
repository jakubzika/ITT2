from abstract_instrument import AbstractInstrument
from object_registry import objectRegistry
from ratio_instrument import RatioInstrument

class Instruments:

  instruments:dict[str, RatioInstrument] = {}

  def __init__(self):
    pass
  
  def gather_data(self):
    pass

  def register_instrument(self, instrument: AbstractInstrument):
    self.instruments[instrument.get_id()] = instrument

  def init_instruments(self):
    self.register_instrument(RatioInstrument("ratio_instrument"))
  