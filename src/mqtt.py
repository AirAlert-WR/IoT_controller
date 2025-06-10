import logging
from enum import StrEnum
import json
import ssl

import paho.mqtt.client as mqtt

from src.mqttTasks.base import AbstractMQTTTask
from src.utils.configuration import AbstractConfigurable


class MQTTManager(AbstractConfigurable):
    """
    Class for providing mqtt functionality
    """

    class _MQTTConfigKeys(StrEnum):
        """
        Enum with keys for reading the configuration
        """
        CLIENT_ID       = "client_id"

        SERVER_HOST     = "server_host"
        SERVER_PORT     = "server_port"

        CERT_PUBLIC     = "cert_public_path"
        CERT_PRIVATE    = "cert_private_path"
        ROOT_CA         = "ca_root_path"


    def __init__(self, config: dict[str,any], tasks: list[AbstractMQTTTask], with_tls: bool = False) -> None:
        """
        Custom constructor for the class

        :param config: the global configuration
        :param tasks: tasks to add for messaging (topics and actions)
        """
        # Call the super constructor
        super().__init__(config)

        keys = self._MQTTConfigKeys

        # Saving some data to protected attributes
        self._client_id = self._config[keys.CLIENT_ID]
        self._task_dictionary = {f"{self._client_id}/{task.topic}": task for task in tasks} # Attention: special mapping
        self._connect_host = self._config[keys.SERVER_HOST]
        self._connect_port = self._config[keys.SERVER_PORT]

        # creating and configuring the mqtt client
        self._client = mqtt.Client(
            client_id   = self._client_id,
        )
        if with_tls:    # Optionally deactivate tls if not necessary
            self._client.tls_set(
                ca_certs    = self._config[keys.CERT_PUBLIC],
                certfile    = self._config[keys.CERT_PRIVATE],
                keyfile     = self._config[keys.ROOT_CA],
                cert_reqs   = ssl.CERT_REQUIRED,
                tls_version = ssl.PROTOCOL_TLSv1_2,
                ciphers     = None
            )

        # Setting internal methods for mqtt client
        self._set_methods_for_internal_client()


    def _set_methods_for_internal_client(self) -> None:
        """
        INTERNAL: setter for event methods, specialized on the internal client
        """

        def event_on_connect(client: mqtt.Client, userdata, flags, rc: int):
            """
            called on connecting
            """
            if rc == 0:
                # print success
                logging.info("HINT (MQTTManager): Connection established")

                # Subscribe to all topics and add manager parameter as parent
                for topic_name in self._task_dictionary.keys():
                    client.subscribe(
                        topic   = topic_name
                    )
                    self._task_dictionary[topic_name].manager = self

            else:
                # else print error
                logging.error(f"ERROR (MQTTManager): Connection not successful, Code {rc}")

        def event_on_disconnect(client: mqtt.Client, userdata, rc: int):
            """
            called on disconnecting
            """
            # Stopping the internal thread
            client.loop_stop()
            # Logging
            if rc == 0:
                logging.info("HINT (MQTTManager): Client disconnected")
            else:
                logging.error(f"ERROR (MQTTManager): Disconnection failure, Code {rc}")

        def event_on_message(client: mqtt.Client, userdata, message: mqtt.MQTTMessage):
            """
            called on receiving a message for a subscribed topic
            """
            try:
                # Fetching topic and raw payload from message
                topic = message.topic
                payload_raw = message.payload.decode("utf-8")
                # Logging
                logging.info(f"HINT (MQTTManager): Message received for topic {topic}: {payload_raw}")

                # Convert json to dictionary
                data_dict: dict = json.loads(payload_raw)

                # Execute task associated to topic
                self._task_dictionary[topic].process_mqtt_task(data_dict)
            except json.JSONDecodeError:
                # Log on exception
                logging.error(f"ERROR (MQTTManager): Failed to decode json.")
            except Exception as e:
                # Log on exception
                logging.error(f"ERROR (MQTTManager): Message gathering problem \n{e}")


        # setting internal event listeners
        self._client.on_connect     = event_on_connect
        self._client.on_disconnect  = event_on_disconnect
        self._client.on_message     = event_on_message


    def connect(self) -> None:
        """
        Method for attempting a server connection.
        """

        #TEMP TODO
        self._client.on_log = lambda c, u, l, s: print("LOG paho:", s)

        # Performing the connection
        self._client.connect(
            host    = self._connect_host,
            port    = self._connect_port
        )
        # Starting the internal thread
        self._client.loop_start()


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
        # Absolute topic
        full_topic = f"{self._client_id}/{topic}"
        # Checking for topic validity
        if full_topic not in self._task_dictionary.keys():
            logging.error(f"ERROR (MQTTManager): Topic {topic} not registered")
            return

        # Converting data to json
        data_json = json.dumps(data)

        # Publishing the content
        self._client.publish(
            topic   = full_topic,
            payload = data_json
        )
        # Logging
        logging.info(f"HINT (MQTTManager): Message sent on {topic}")

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
            keys.CLIENT_ID       : loaded_config.get(keys.CLIENT_ID,    ""),
            keys.CERT_PUBLIC    : loaded_config.get(keys.CERT_PUBLIC,   "certs/public.pem"),
            keys.CERT_PRIVATE   : loaded_config.get(keys.CERT_PRIVATE,  "certs/private.key"),
            keys.ROOT_CA        : loaded_config.get(keys.ROOT_CA,       "certs/root_ca.pem"),
            keys.SERVER_HOST    : loaded_config.get(keys.SERVER_HOST,   "127.0.0.1"),
            keys.SERVER_PORT    : int(p) if (p := loaded_config.get(keys.SERVER_PORT, "3181")).isdigit() else 3181
        }
