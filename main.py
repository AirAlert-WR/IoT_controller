from src.utils import ConfigurationReader
from src.mqtt import MQTTManager

from src.mqtttasks.base import AbstractMQTTTask
from src.mqtttasks.texttospeech import TextToSpeech
from src.mqtttasks.sensors import SensorManager

from src.mqtttasks.sensordevices.base import AbstractSensorDevice
from src.mqtttasks.sensordevices.mq135 import SensorMQ135
from src.mqtttasks.sensordevices.sds011 import SensorSDS011

if __name__ == "__main__":
    """
    Application entry
    """

    # Register Sensors
    sensors: list[AbstractSensorDevice] = [
        SensorMQ135(),
        SensorSDS011()
    ]

    # Register application parts
    tasks: list[AbstractMQTTTask] = [
        SensorManager(sensors),
        TextToSpeech()
    ]

    # Load the configuration reader
    config = ConfigurationReader("config.ini")

    # Load the mqtt manager
    manager = MQTTManager(
        config  = config.for_section("mqtt"),
        tasks   = tasks
    )
    # Connect the manager
    manager.connect()