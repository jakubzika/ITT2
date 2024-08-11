import asyncio
import rerun as rr
import serial
from typing import Tuple

from .registry import sensorRegistry
from .entity import SensorEntity

class SensorsManager:

    def __init__(self):
        self.init_sensors()

    async def start_service(self):
        print("starting SensorsManager")
        while True:
            try:
                serial_port = serial.Serial(port = "/dev/ttys021", baudrate = 9600,
                                timeout=2, stopbits=serial.STOPBITS_ONE)
                while True:
                    # print('cycle')
                    await asyncio.sleep(0.05)
                    
                    serial_data = None

                    while(serial_port.in_waiting != 0):
                        serial_data = serial_port.readline()

                    if serial_data == None:
                        continue

                    
                    serial_string = serial_data.decode('Ascii').rstrip()
                    pairs = self.parse_serial_input(serial_string)
                    self.update_sensors(pairs)

            except Exception as e:
                print('error')
                print(e)

            print("finished")

        print("ended SensorsManager")

    def update_sensors(self, pairs: Tuple[str, int]):
        for sensor_id, reading in pairs:
            sensor_entity = sensorRegistry.get(sensor_id)
            sensor_entity.reading = reading


    def parse_serial_input(self, serial_string) -> Tuple[str, int]:
        items = serial_string.split(',')
        pairs = [item.split(':') for item in items]
        parsed_pairs = [(pair[0], int(pair[1])) for pair in pairs]
        return parsed_pairs

    def init_sensors(self):
        sensorRegistry.add(
            SensorEntity(id="Dist0", reading=0),
            SensorEntity(id="Dist1", reading=0),
            SensorEntity(id="Dist2", reading=0),
            SensorEntity(id="Dist3", reading=0),
            SensorEntity(id="Dist4", reading=0),
            SensorEntity(id="Dist5", reading=0),
        )
