# Internal variable for saving support platform
from src.utils.det_platform import classify_host, EnumPlatform
_platform_supported = classify_host() in [EnumPlatform.RASPBERRY_PI]

# Importing / Creating the internal wrapper
try:
    from board import SCL as SCL, SDA as SDA
    from busio import I2C as I2C
    from adafruit_ads1x15.ads1115 import ADS1115 as ADC
    from adafruit_ads1x15.analog_in import AnalogIn as AnalogIn
except ImportError:
    # Platform not supported
    _platform_supported = False
    # Dummy implementation (ATTENTION: may be not equal to the original one)
    SCL = SDA = object()
    class I2C:
        def __init__(self,scl,sda): pass
    class ADC:
        def __init__(self,i2c: I2C,gain: int): pass
    class AnalogIn:
        def __init__(self,ads: ADC,positive_pin: int): pass
        @property
        def voltage(self): return 0

class ADCInput:
    """
    Class for providing a custom analog input wrapper
    """

    def __init__(self, ain: AnalogIn):
        """
        Custom constructor
        """
        self._ain = ain

    @property
    def voltage(self) -> float:
        """
        :return: The voltage measured at the specific port
        """
        return self._ain.voltage

class ADCSingleton:
    _NUM_PORTS = 4
    """
    Constant for saving the maximum amount of reserved ports
    """
    _adc: ADC | None = None
    _channels: dict[int,ADCInput] = {}
    """
    Variables for managing the singleton's functionality
    """

    @classmethod
    def _create_adc(cls, gain: int = 1) -> None:
        """
        Static method for creating the internal converter object
        :param gain: the gain to read the analog values with
        """
        if cls._adc is None:
            i2c = I2C(SCL, SDA)
            cls._adc = ADC(i2c,gain = gain)

    @classmethod
    def get_for_port(cls, port: int) -> ADCInput | None:
        """
        Static method for obtaining an analog input for a port number
        :param port: the channel of the adc to read
        :return: None if error or not supported; else an input Object
        """
        # Return None if platform not supported
        if not _platform_supported: return None

        # Return None if port invalid
        p_range = range(cls._NUM_PORTS)
        if port not in p_range:
            print(f"ERROR (ADCSingleton): the port number should be inside {p_range}")
            return None

        # create the internal converter
        cls._create_adc()

        # Create new input object (if port not already saved)
        if port not in cls._channels:
            ain = AnalogIn(cls._adc,port)
            inp = ADCInput(ain)
            cls._channels[port] = inp
        # Returning the object from the dictionary
        return cls._channels[port]