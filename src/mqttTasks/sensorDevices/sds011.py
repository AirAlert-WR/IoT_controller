# Internal variable for saving support platform
from src.utils.det_platform import classify_host, EnumPlatform
_platform_supported = classify_host() in [EnumPlatform.RASPBERRY_PI]

# Importing / Creating the internal wrapper
try:
    from sds011lib import SDS011QueryReader as SDS011Reader
except ImportError:
    # Platform not supported
    _platform_supported = False
    # Dummy implementation (ATTENTION: may be not equal to the original one)
    class SDS011Reader:
        def __init__(self,*args): pass
        def set_working_period(self,_): pass
        @staticmethod
        def query(): return QueryResponse()
    class QueryResponse:
        @property
        def pm25(self): return 0
        @property
        def pm10(self): return 0

from src.mqttTasks.sensorDevices.base import AbstractSensorDevice
class SensorSDS011(AbstractSensorDevice):
    """
    Class with the SDS011 sensor implementation
    """

    from enum import StrEnum
    class SensorSDS011Keys(StrEnum):
        """
        Enum with keys for setting the sensor data dictionary
        """
        pm2_5 = "pm2_5"
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
            self._sensor_sds011 = SDS011Reader('/dev/ttyUSB0')
            self._sensor_sds011.set_working_period(0)

    @property
    def id(self) -> str:
        return "sds011"

    def measure(self) -> None:

        # Setting the data space
        if self._is_dummy:
            import random
            # Random values, if dummy
            self._data[self.SensorSDS011Keys.pm2_5] = random.uniform(5,30)  # µg/m^3
            self._data[self.SensorSDS011Keys.pm10] = random.uniform(10,50)  # µg/m^3
        else:
            # From query-Result
            query_result: QueryResponse = self._sensor_sds011.query()
            self._data[self.SensorSDS011Keys.pm2_5] = query_result.pm25
            self._data[self.SensorSDS011Keys.pm10] = query_result.pm10