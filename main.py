from configparser import ConfigParser

from src.utils import DEF_CONFIG_FILE
from src.mqtt import MQTTManager

from src.mqttTasks.base import AbstractMQTTTask
from src.mqttTasks.texttospeech import TextToSpeech
from src.mqttTasks.sensors import SensorManager

from src.mqttTasks.sensorDevices.base import AbstractSensorDevice
from src.mqttTasks.sensorDevices.mq135 import SensorMQ135
from src.mqttTasks.sensorDevices.sds011 import SensorSDS011

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
    config_reader = ConfigParser()
    config_reader.read(DEF_CONFIG_FILE)
    config = dict(config_reader[MQTTManager.section()])

    # Load the mqtt manager
    manager = MQTTManager(
        config  = config,
        tasks   = tasks
    )
    # Connect the manager
    manager.connect()