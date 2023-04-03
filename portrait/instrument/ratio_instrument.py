import math

from abstract_instrument import AbstractInstrument
from object_registry import objectRegistry
from camera_object import ObjectCategory

class RatioInstrument(AbstractInstrument):

  ratio = 0
  instrument_id = ""

  def __init__(self, instrument_id):
    self.instrument_id = instrument_id
    
  def update(self):
    num_nature_objects = 0
    num_city_objects = 0

    for obj in objectRegistry.get_all_camera_objects():
      if obj.category is ObjectCategory.CITY:
        num_city_objects += 1
      elif obj.category is ObjectCategory.NATURE:
        num_nature_objects += 1

    max_category = ObjectCategory.CITY if num_city_objects >= num_nature_objects else ObjectCategory.NATURE
    max_val = max(num_city_objects, num_nature_objects)

    sharpness = 1
    softmax_sum = math.exp(sharpness * num_nature_objects) + math.exp(sharpness * num_city_objects)
    softmax = math.exp(sharpness * num_nature_objects) / softmax_sum

    return super().update()

  def get_data(self):
    return self.ratio
  
  def get_id(self):
    return self.instrument_id