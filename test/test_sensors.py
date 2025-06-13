import unittest
from time import sleep

from src.mqttTasks.sensorDevices.scd41 import SensorSCD41
from src.mqttTasks.sensorDevices.sds011 import SensorSDS011


class MyTestCase(unittest.TestCase):

    def test_sensor_scd41(self):
        sensor_scd41 = SensorSCD41()

        print("\nTest sensor scd41\n")

        for counter in range(10):
            sensor_scd41.measure()
            print(sensor_scd41.data)
            sleep(1)

    def test_sensor_sds011(self):
        sensor_sds011 = SensorSDS011()

        print("\nTest sensor sds011\n")

        for counter in range(10):
            sensor_sds011.measure()
            print(sensor_sds011.data)
            sleep(1)

    def test_enum_validity(self):

        print("\nTest enum validity\n")

        enum_value = SensorSDS011.SensorSDS011Keys.pm10

        self.assertEqual(enum_value,str(enum_value),"Enum to string conversions are not equal")


if __name__ == '__main__':
    unittest.main()
