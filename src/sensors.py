import platform
import enum
from typing import Callable

SENSOR_DEBUGGING = False
"""
A debug mode flag for setting random instead of sensor value
"""
# Checking for supported device
_IS_PI = (platform.machine().startswith("arm") and "raspberrypi" in platform.uname().node.lower())
# Attempting to import
try:
    import board
    import busio
    from adafruit_ads1x15.ads1115 import ADS1115
    from adafruit_ads1x15.analog_in import AnalogIn
    from sds011 import SDS011
    _SENSOR_IMPLEMENTATION_AVAILABLE = True
except ImportError:
    import random
    _SENSOR_IMPLEMENTATION_AVAILABLE = False

# If not Pi or Sensor Libraries not loaded: DEBUGGING
if not _IS_PI or not _SENSOR_IMPLEMENTATION_AVAILABLE:
    print("Warning [sensors.py]: Sensors are not active; debug values used instead.")
    SENSOR_DEBUGGING = True

class SensorKey(enum.StrEnum):
    """
    Enum with sensor identifiers for accessing them
    """
    SENSOR_MQ135 = "mq135"
    SENSOR_SDS011_PM2_5 = "sds011_PM2_5"
    SENSOR_SDS011_PM10 = "sds011_PM10"

class SensorManager:
    """
    Class for providing functionality to fetch sensor measuring data
    """

    def __init__(self):
        pass

        # Creating the internal sensors


        self.callbackOnReady: Callable[[], None] = lambda: None
        """
        Method reference to call if the measuring task was finished
        """

        self.data: dict[SensorKey,float] = {}
        """
        Structure consisting of sensor data values.
        Filled when perform_measuring is called
        """

    def perform_measuring(self):
        pass





def initialize() -> None:
    """
        Helping
    """
    pass

def perform_measuring() -> None:
    """

    :return:
    """
    callbackOnReady()
