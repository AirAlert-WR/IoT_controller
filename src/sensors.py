import json
import platform
import enum
from typing import Callable

from src.mqtt import MQTTManager, MQTTTaskClass

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

class SensorManager(MQTTTaskClass):
    """
    Class for providing functionality to fetch sensor measuring data
    """

    def __init__(self):
        """
        Custom constructor for the text-to-speech class
        """
        # Call constructor of mother class
        super().__init__()

        # TODO Creating the internal sensors


        self.callbackOnReady: Callable[[], None] = lambda: None
        """
        Method reference to call if the measuring task was finished
        """

        self.data: dict[SensorKey,float] = {}
        """
        Structure consisting of sensor data values.
        Filled when perform_measuring is called
        """

    def _perform_measuring(self):
        pass

    '''
    Methods to override
    '''
    def get_topic(self) -> str:
        return "sensor"

    def process(self, data_json: str = "") -> None:
        ## Attention: Data not important!!!

        # Perform measuring routine
        self._perform_measuring()

        # Collecting and converting the data to json
        data_json = json.dumps(self.data)
        # Calling the publish Method of the associated mqtt manager
        if self.mqtt_manager is not None:
            self.mqtt_manager.submit(
                topic       = self.get_topic(),
                data_json   = data_json
            )