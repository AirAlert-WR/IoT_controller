# Internal variable for saving support platform
from src.utils.det_platform import classify_host, EnumPlatform
_platform_supported = classify_host() in [EnumPlatform.RASPBERRY_PI]

# TODO scd41 import
# Importing / Creating the internal wrapper
try:
    from board import SCL as SCL, SDA as SDA
    from busio import I2C as I2C
    from adafruit_scd4x import SCD4X as SCD41Reader
except ImportError:
    # Platform not supported
    _platform_supported = False
    # Dummy implementation (ATTENTION: may be not equal to the original one)
    SCL = SDA = object()
    class I2C:
        def __init__(self,scl,sda): pass
    class SCD41Reader:
        def __init__(self,i2c: I2C): pass
        def stop_periodic_measurement(self): pass
        def perform_single_measurement(self): pass
        @property
        def data_ready(self): return True
        @property
        def CO2(self): return 0.0
        @property
        def temperature(self): return 0.0
        @property
        def relative_humidity(self): return 0.0

import time
from src.mqttTasks.sensorDevices.base import AbstractSensorDevice
class SensorSCD41(AbstractSensorDevice):
    """
    Class with the SCD41 sensor implementation
    """

    from enum import StrEnum
    class SensorSCD41Keys(StrEnum):
        """
        Enum with keys for setting the sensor data dictionary
        """
        temperature = "temperature"
        co2 = "co2"
        humidity = "humidity"

    def __init__(self,is_dummy: bool = False):

        # Calling the constructor of the mother class (including the restriction)
        super().__init__(
            is_dummy    = is_dummy | (not _platform_supported)
        )

        # Initializing the data as a dictionary
        self._data: dict[str,any] = {
            str(self.SensorSCD41Keys.co2): 0.0,
            str(self.SensorSCD41Keys.temperature): 0.0,
            str(self.SensorSCD41Keys.humidity): 0.0
        }

        # Setting up the sensor (if not dummy)
        if not self._is_dummy:
            i2c = I2C(SCL, SDA)
            self._sensor_scd41 = SCD41Reader(i2c)
            self._sensor_scd41.stop_periodic_measurement()

    @property
    def id(self) -> str:
        return "scd41"

    def measure(self) -> None:

        # Setting the data space
        if self._is_dummy:
            import random
            # Random values, if dummy
            self._data[self.SensorSCD41Keys.co2] = random.uniform(500, 2000)        # ppm
            self._data[self.SensorSCD41Keys.temperature] = random.uniform(10, 35)   # °C
            self._data[self.SensorSCD41Keys.humidity] = random.uniform(20, 90)      # %RH
        else:
            # Get measurement and sleep for 5s
            self._sensor_scd41.perform_single_measurement()
            while not self._sensor_scd41.data_ready:
                time.sleep(0.5)
            # Set from reader properties
            self._data[self.SensorSCD41Keys.co2] = self._sensor_scd41.CO2
            self._data[self.SensorSCD41Keys.temperature] = self._sensor_scd41.temperature
            self._data[self.SensorSCD41Keys.humidity] = self._sensor_scd41.relative_humidity