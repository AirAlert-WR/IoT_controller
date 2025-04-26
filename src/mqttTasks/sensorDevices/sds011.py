import enum

from src.utils import is_raspberrypi
from src.mqttTasks.sensorDevices.base import AbstractSensorDevice

# Restrict for supported platform
_platform_supported = is_raspberrypi()
# Check for import errors
try:
    from sds011 import SDS011
except ImportError:
    import random
    _platform_supported = False

class SensorSDS011(AbstractSensorDevice):
    """
    Class with the SDS011 sensor implementation
    """

    class SensorSDS011Keys(enum.StrEnum):
        """
        Enum with keys for setting the sensor data dictionary
        """
        pm2_5 = "pm2.5"
        pm10 = "pm10"

    def __init__(self,is_dummy: bool = False):

        # Calling the constructor of the mother class (including the restriction)
        super().__init__(
            is_dummy    = is_dummy | (not _platform_supported)
        )

        # Initializing the data as a dictionary
        self._data: dict[str,any] = {
            str(self.SensorSDS011Keys.pm2_5): 0.0,
            str(self.SensorSDS011Keys.pm10): 0.0
        }

        # Setting up the sensor (if not dummy)
        if not self._is_dummy:
            self._sensor_sds011 = SDS011("/dev/ttyUSB0")
            self._sensor_sds011.set_working_period(0)

    @property
    def id(self) -> str:
        return "sds011"

    def measure(self) -> None:

        # Setting the data space
        if self._is_dummy:
            # Random values, if dummy
            self._data[self.SensorSDS011Keys.pm2_5] = random.uniform(5, 50)
            self._data[self.SensorSDS011Keys.pm10] = random.uniform(10, 100)
        else:
            self._data[self.SensorSDS011Keys.pm2_5], self._data[self.SensorSDS011Keys.pm10] = self._sensor_sds011.query()