from src.utils.config import load_config, DEF_CONF_FILE
from src.mqtt import MQTTManager, MQTTTaskClass

from src.audio import TextToSpeech
from src.sensors import SensorManager

if __name__ == "__main__":
    """
    Application entry
    """

    # Register application parts
    tasks: list[MQTTTaskClass] = [
        SensorManager(),
        TextToSpeech()
    ]

    # Load the mqtt manager (config + instance)
    mqtt_config = load_config(
        filename = DEF_CONF_FILE,
        section = "mqtt"
    )
    mqtt_manager = MQTTManager(mqtt_config,tasks)

    mqtt_manager.connect()

