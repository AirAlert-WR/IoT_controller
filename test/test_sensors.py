import unittest
from time import sleep

# Fix code for imports
import os, sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Own imports
from src.mqttTasks.sensorDevices.scd41 import SensorSCD41
from src.mqttTasks.sensorDevices.sds011 import SensorSDS011


class MyTestCase(unittest.TestCase):
    """
    Class for providing an opportunity to test code
    """

    def test_sensor_scd41(self):
        """
        Method for testing the SCD41 implementation correctness
        """

        # Creating the sensor object
        sensor_scd41 = SensorSCD41()
        print("\nTest sensor scd41\n")

        # Fetching the current sensor data for 10 times
        for counter in range(10):
            sensor_scd41.measure()
            print(sensor_scd41.data)
            sleep(1)

    def test_sensor_sds011(self):
        """
        Method for testing the SCD41 implementation correctness
        """

        # Creating the sensor object
        sensor_sds011 = SensorSDS011()
        print("\nTest sensor sds011\n")

        # Fetching the current sensor data for 10 times
        for counter in range(10):
            sensor_sds011.measure()
            print(sensor_sds011.data)
            sleep(1)

    def test_enum_validity(self):
        """
        Method for testing the (generally any) Sensor data key enum (in terms of transcription correctness)
        ATTENTION: Enum value should be a string!!!
        """

        print("\nTest enum validity\n")
        # Obtaining any enum value
        enum_value = SensorSDS011.SensorSDS011Keys.pm10
        # Asserting the non-successful conversion to string
        self.assertEqual(enum_value,str(enum_value),"Enum to string conversions are not equal")


if __name__ == '__main__':
    """
    Application entry
    """
    # Special code automation: running all methods of this class AUTOMATICALLY, so everything gets "tested"
    unittest.main()
