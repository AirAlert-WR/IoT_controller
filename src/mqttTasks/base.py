from abc import ABC, abstractmethod

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
    def process_mqtt_task(self, data: dict) -> None:
        """
        Method for processing the integrated task for the mqtt manager
        :param data: the data dictionary for custom parsing inside the functionality
        """
        pass