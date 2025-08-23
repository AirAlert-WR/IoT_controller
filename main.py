import time

from src.utils.configuration import AbstractConfigurable, GlobalConfiguration

from src.mqtt import MQTTManager
from src.mqttTasks.base import AbstractMQTTTask
from src.mqttTasks.sensors import SensorManager
from src.mqttTasks.sensorDevices.base import AbstractSensorDevice
from src.mqttTasks.sensorDevices.sds011 import SensorSDS011
from src.mqttTasks.sensorDevices.scd41 import SensorSCD41

import logging
logging.basicConfig(
    level=logging.INFO,  # ⬅️ Zeigt auch debug-Ausgaben
    format="%(levelname)s (%(name)s): %(message)s"
)

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
        SensorSCD41(),
        SensorSDS011()
    ]

    # Register MQTTTasks
    tasks: list[AbstractMQTTTask] = [
        SensorManager(sensors)
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

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        manager.disconnect()