import unittest
from time import sleep

from src.mqttTasks.sensorDevices.mq135 import SensorMQ135
from src.mqttTasks.sensorDevices.sds011 import SensorSDS011


class MyTestCase(unittest.TestCase):

    def test_sensor_mq135(self):
        sensor_mq135 = SensorMQ135()

        print("\nTest sensor mq135\n")

        for counter in range(10):
            sensor_mq135.measure()
            print(sensor_mq135.data)
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
