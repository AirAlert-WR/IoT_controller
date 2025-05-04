from src.utils.configuration import AbstractConfigurable, GlobalConfiguration

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

    # Collect all used configuration objects
    list_of_configurables: list[type[AbstractConfigurable]] = [
        MQTTManager
    ]

    # Load and correct the configurations
    configuration = GlobalConfiguration()
    configuration.correct_configuration(list_of_configurables)
    configuration.save()

    # Register Sensors
    sensors: list[AbstractSensorDevice] = [
        SensorMQ135(),
        SensorSDS011()
    ]

    # Register MQTTTasks
    tasks: list[AbstractMQTTTask] = [
        SensorManager(sensors),
        TextToSpeech()
    ]

    # Fetch the configuration for the mqtt manager
    mqtt_config = configuration.for_configurable(MQTTManager)

    # Load the mqtt manager (with according configuration)
    manager = MQTTManager(
        config  = mqtt_config,
        tasks   = tasks
    )
    # Connect the manager
    manager.connect()