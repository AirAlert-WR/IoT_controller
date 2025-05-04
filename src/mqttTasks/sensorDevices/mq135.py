from src.mqttTasks.sensorDevices.ad_helper import ADCSingleton, ADCInput

from src.mqttTasks.sensorDevices.base import AbstractSensorDevice
class SensorMQ135(AbstractSensorDevice):
    """
    Class with the MQ135 sensor implementation
    """

    def __init__(self,is_dummy: bool = False):

        # Calling the constructor of the mother class (including the restriction)
        super().__init__(
            is_dummy    = is_dummy
        )

        # Trying to load through the analog input
        inp: ADCInput = ADCSingleton.get_for_port(0)
        # Setting dummy mode (if not successful)
        if inp is None:
            print(f"WARNING (SensorMQ135): Input not loaded; switching to dummy configuration.")
            self._is_dummy = True
            return

        # Else: saving as attribute
        self._sensor_mq135 = inp

    @property
    def id(self) -> str:
        return "mq135"

    def measure(self) -> None:
        # Setting the data space
        if self._is_dummy:
            import random
            # Random values, if dummy
            self._data = random.uniform(100,300)
        else:
            self._data = self._sensor_mq135.voltage