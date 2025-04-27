from enum import StrEnum
import json
import ssl

import paho.mqtt.client as mqtt

from src.mqttTasks.base import AbstractMQTTTask
from src.utils import AbstractConfigurable


class MQTTManager(AbstractConfigurable):
    """
    Class for providing mqtt functionality
    """

    class _MQTTConfigKeys(StrEnum):
        """
        Enum with keys for reading the configuration
        """
        USER_NAME       = "username"
        USER_PASSWORD   = "password"
        USER_ID         = "id"

        SERVER_HOST     = "host"
        SERVER_PORT     = "port"

        CERT_ROOT       = "ca_root"
        CERT_MAIN       = "ca_main"
        CERT_KEY        = "key_private"


    def __init__(self, config: dict[str,any], tasks: list[AbstractMQTTTask]) -> None:
        """
        Custom constructor for the class

        :param config: the global configuration
        :param tasks: tasks to add for messaging (topics and actions)
        """
        # Call the super constructor
        super().__init__(config)

        keys = self._MQTTConfigKeys

        # creating and configuring the mqtt client
        self._client = mqtt.Client(
            client_id   = self._config[keys.USER_ID],
            #userdata    = None,
            #protocol    = mqtt.MQTTv5
        )
        self._client.tls_set(
            ca_certs    = self._config[keys.CERT_ROOT],
            certfile    = self._config[keys.CERT_MAIN],
            keyfile     = self._config[keys.CERT_KEY],
            tls_version = ssl.PROTOCOL_TLSv1_2
        )
        self._client.tls_insecure_set(False)
        self._client.username_pw_set(
            username    = self._config[keys.USER_NAME],
            password    = self._config[keys.USER_PASSWORD]
        )

        # Saving some data to protected attributes
        self._task_dictionary = {task.topic: task for task in tasks}
        self._connect_host = self._config[keys.SERVER_HOST]
        self._connect_port = self._config[keys.SERVER_PORT]

        # Setting internal methods for mqtt client
        self._set_methods_for_internal_client()


    def _set_methods_for_internal_client(self) -> None:
        """
        INTERNAL: setter for event methods, specialized on the internal client
        """

        def event_on_connect(client: mqtt.Client, rc: int):
            """
            called on connecting
            """
            if rc == 0:
                # print success
                print("HINT (MQTTManager): Connection established")

                # Subscribe to all topics and add manager parameter as parent
                for task in self._task_dictionary.values():
                    client.subscribe(
                        topic   = task.topic
                    )
                    task.manager = self

            else:
                # else print error
                print(f"ERROR (MQTTManager): Connection not successful, Code {rc}")

        def event_on_subscribe(client: mqtt.Client, userdata, mid: int, granted_quos):
            """
            called on subscribing to a topic
            """
            #topics = list(MQTTTopic)
            #TODO print message
            pass

        def event_on_publish(client: mqtt.Client, userdata, mid: int):
            """
            called on subscribing to a topic
            """
            #TODO print message
            pass

        def event_on_disconnect(rc: int):
            """
            called on disconnecting
            """
            # Logging
            if rc == 0:
                print("HINT (MQTTManager): Client disconnected")
            else:
                print(f"ERROR (MQTTManager): Disconnection failure, Code {rc}")

        def event_on_message(message: mqtt.MQTTMessage):
            """
            called on receiving a message for a subscribed topic
            """
            try:
                # Fetching topic and raw payload from message
                topic = message.topic
                payload_raw = message.payload.decode("utf-8")
                # Logging
                print(f"HINT (MQTTManager): Message received for topic {topic}")

                # Convert json to dictionary
                data_dict: dict = json.loads(payload_raw)

                # Execute task associated to topic
                self._task_dictionary[topic].process_mqtt_task(data_dict)
            except json.JSONDecodeError:
                # Log on exception
                print(f"ERROR (MQTTManager): Failed to decode json.")
            except Exception as e:
                # Log on exception
                print(f"ERROR (MQTTManager): Message gathering problem \n{e}")


        # setting internal event listeners
        self._client.on_connect     = event_on_connect
        self._client.on_subscribe   = event_on_subscribe
        self._client.on_publish     = event_on_publish
        self._client.on_disconnect  = event_on_disconnect
        self._client.on_message     = event_on_message


    def connect(self) -> None:
        """
        Method for attempting a server connection.
        """
        # Performing the connection
        self._client.connect(
            host    = self._connect_host,
            port    = self._connect_port
        )
        # Starting the internal thread
        self._client.loop_forever()


    def disconnect(self) -> None:
        """
        Method for disconnecting from the client
        """
        self._client.disconnect()


    def submit(self, topic: str, data: dict) -> None:
        """
        Method for sending a message to the connected mqtt server

        :param topic: topic identifier to submit on
        :param data: data dictionary to submit
        """
        # Checking for topic validity
        if topic not in self._task_dictionary.keys():
            print(f"ERROR (MQTTManager): Topic {topic} not registered")
            return

        # Converting data to json
        data_json = json.dumps(data)

        # Publishing the content
        self._client.publish(
            topic   = topic,
            payload = data_json
        )

    '''
    Methods to override
    '''
    @classmethod
    def section(cls) -> str:
        return "mqtt"

    @classmethod
    def mod_config(cls, loaded_config: dict[str,any]) -> dict[str,any]:

        keys = cls._MQTTConfigKeys
        return {
            keys.USER_NAME      : loaded_config.get(keys.USER_NAME,     ""),
            keys.USER_PASSWORD  : loaded_config.get(keys.USER_PASSWORD, ""),
            keys.USER_ID        : loaded_config.get(keys.USER_ID,       ""),
            keys.CERT_ROOT      : loaded_config.get(keys.CERT_ROOT,     "certs/mqtt.ca"),
            keys.CERT_MAIN      : loaded_config.get(keys.CERT_MAIN,     "certs/mqtt.crt"),
            keys.CERT_KEY       : loaded_config.get(keys.CERT_KEY,      "certs/mqtt.key"),
            keys.SERVER_HOST    : loaded_config.get(keys.SERVER_HOST,   "127.0.0.1"),
            keys.SERVER_PORT    : int(p) if (p := loaded_config.get(keys.SERVER_PORT, "3181")).isdigit() else 3181
        }
