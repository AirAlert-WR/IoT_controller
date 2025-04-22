from src.mqtt import MQTTManager
from src.utils.config import load_config, DEF_CONF_FILE

if __name__ == "__main__":
    """
    Application entry
    """
    # Load the mqtt manager (config + instance)
    mqtt_config = load_config(
        filename = DEF_CONF_FILE,
        section = "mqtt"
    )
    mqtt_manager = MQTTManager(mqtt_config)
