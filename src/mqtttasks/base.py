from abc import ABC, abstractmethod
#from src.mqtt import MQTTManager

class AbstractMQTTTask(ABC):
    """
    ABSTRACT: Base class for tasks using the MQTTManager
    """

    def __init__(self) -> None:
        self.manager: any = None

    @property
    def manager(self):
        """
        :return: the associated mqtt manager
        """
        return self._manager

    @manager.setter
    def manager(self, value: any) -> None:
        """
        Method for setting an associated mqtt manager
        """
        self._manager = value

    @property
    @abstractmethod
    def topic(self) -> str:
        """
        :return: a constant topic string for the associated task
        """
        pass

    @abstractmethod
    def process_mqtt_task(self, data_json: str = "") -> None:
        """
        Method for processing the integrated task for the mqtt manager
        :param data_json: the json-encoded data to use for the task
        """
        pass