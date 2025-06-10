import logging

from src.mqttTasks.base import AbstractMQTTTask
from src.mqttTasks.sensorDevices.base import AbstractSensorDevice

class SensorManager(AbstractMQTTTask):
    """
    Class for providing functionality to fetch sensor measuring data
    """

    def __init__(self, sensors: list[AbstractSensorDevice]) -> None:
        """
        Custom constructor for the text-to-speech class
        :param sensors: A collection of sensors to measure
        """
        # Call constructor of mother class
        super().__init__()

        self._sensors = sensors
        self._data: dict[str,any] = {}

    @property
    def data(self):
        """
        :return: the recent data dictionary consisting of the sensor values
        """
        return self._data


    def perform_measuring(self):
        # Place every measuring result into the dictionary
        for sensor in self._sensors:
            sensor.measure()

            #self._data[sensor.id] = sensor.data
            # Save FLATTENED data inside the dict
            self._data.update(sensor.data)

    '''
    Methods for MQTTTaskClass
    '''
    @property
    def topic(self) -> str:
        return "sensor"

    def process_mqtt_task(self, data: dict) -> None:

        ## Attention: data parameter ignored

        # Perform measuring routine
        self.perform_measuring()

        # Calling the publish Method of the associated mqtt manager
        if self._manager is not None:

            self._manager.submit(
                topic   = self.topic,
                data    = self.data
            )