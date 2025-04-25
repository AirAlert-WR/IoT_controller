from src.utils import is_raspberrypi
from src.mqtttasks.sensordevices.base import AbstractSensorDevice

# Restrict for supported platform
_platform_supported = is_raspberrypi()
# Check for import errors
try:
    import board
    import busio
    from adafruit_ads1x15.ads1115 import ADS1115
    from adafruit_ads1x15.analog_in import AnalogIn
except ImportError:
    import random
    _platform_supported = False

class SensorMQ135(AbstractSensorDevice):
    """
    Class with the MQ135 sensor implementation
    """

    def __init__(self,is_dummy: bool = False):

        # Calling the constructor of the mother class (including the restriction)
        super().__init__(
            is_dummy    = is_dummy | (not _platform_supported)
        )

        # Setting up the sensor (if not dummy)
        if not self._is_dummy:
            i2c = busio.I2C(board.SCL, board.SDA)
            self._ads = ADS1115(i2c)
            self._sensor_mq135 = AnalogIn(self._ads, ADS1115.P0)

    @property
    def id(self) -> str:
        return "mq135"

    def measure(self) -> None:
        # Setting the data space
        if self._is_dummy:
            # Random values, if dummy
            self._data = random.uniform(100,300)
        else:
            self._data = self._sensor_mq135.voltage