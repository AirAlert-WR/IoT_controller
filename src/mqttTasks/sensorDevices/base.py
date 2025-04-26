from abc import ABC, abstractmethod

class AbstractSensorDevice(ABC):
    """
    ABSTRACT: base class for generic sensor device implementation
    """

    def __init__(self, is_dummy: bool = False) -> None:
        """
        Custom constructor
        :param is_dummy: state if sensor should provide random instead of measuring values
        """

        self._is_dummy = is_dummy
        self._data: any = 0

    @property
    @abstractmethod
    def id(self) -> str:
        """
        :return: a constant topic string for the associated task
        """
        pass

    @property
    def data(self) -> any:
        """
        :return: the most recent measuring data
        """
        return self._data

    @abstractmethod
    def measure(self) -> None:
        """
        Method for starting a measuring cycle
        """