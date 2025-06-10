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
        USER_NAME       = "username"
        USER_PASSWORD   = "password"

        CERT_ROOTCA     = "path_RootCA"
        CERT_DEVCERT    = "path_Certificate"
        CERT_PRIVKEY    = "path_PrivateKey"

        USE_TLS         = "use_tls"

        SERVER_HOST     = "host"
        SERVER_PORT     = "port"

        CLIENT_ID       = "id"


    def __init__(self, config: dict[str,any], tasks: list[AbstractMQTTTask]) -> None:
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
        self._task_dictionary = {task.topic: task for task in tasks}
        self._connect_host = self._config[keys.SERVER_HOST]
        self._connect_port = self._config[keys.SERVER_PORT]

        # creating and configuring the mqtt client
        self._client = mqtt.Client(
            client_id   = self._client_id,
        )

        # Setting tls connection
        if config[keys.USE_TLS]==str(True):    # Optionally deactivate tls if not necessary
            self._client.tls_set(
                ca_certs    = self._config[keys.CERT_ROOTCA],
                certfile    = self._config[keys.CERT_DEVCERT],
                keyfile     = self._config[keys.CERT_PRIVKEY],
                cert_reqs   = ssl.CERT_REQUIRED,
                tls_version = ssl.PROTOCOL_TLSv1_2,
                ciphers     = None
            )
            self._client.tls_insecure_set(False)

        # Setting username and password
        self._client.username_pw_set(
            username    = self._config[keys.USER_NAME],
            password    = self._config[keys.USER_PASSWORD],
        )

        # Setting constant for one main subscribed task
        self.TOPIC_TASK = f"{self._client_id}/task"

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

                # Subscribe to the task topic
                client.subscribe(
                    topic   = self.TOPIC_TASK
                )

                # Setting this Manager instance for all tasks
                for topic_name in self._task_dictionary.keys():
                    self._task_dictionary[topic_name].manager = self
                    # Initial task:
                    logging.info("HINT (MQTTManager): Executing initial commands")
                    self._task_dictionary[topic_name].process_mqtt_task({})




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

                # Getting task name and data
                task_name = data_dict["name"]
                task_data = data_dict.get("data",{})

                # Execute task associated to topic
                self._task_dictionary[task_name].process_mqtt_task(task_data)
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
        # Checking for topic validity
        if topic not in self._task_dictionary.keys():
            logging.error(f"ERROR (MQTTManager): Topic {topic} not registered")
            return

        # Converting data to json
        data_json = json.dumps(data)

        # Creating the full (unique) topic identifier
        full_topic = f"{self._client_id}/{topic}"

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
            keys.USER_NAME      : loaded_config.get(keys.USER_NAME,     ""),
            keys.USER_PASSWORD  : loaded_config.get(keys.USER_PASSWORD, ""),
            keys.CERT_ROOTCA    : loaded_config.get(keys.CERT_ROOTCA,   "certs/rootCA.pem"),
            keys.CERT_DEVCERT   : loaded_config.get(keys.CERT_DEVCERT,  "certs/certificate.pem.crt"),
            keys.CERT_PRIVKEY   : loaded_config.get(keys.CERT_PRIVKEY,  "certs/private.pem.key"),
            keys.USE_TLS        : bool(v) if (v := loaded_config.get(keys.USE_TLS, "false").lower()) in ("1", "true", "yes", "on") else False,
            keys.SERVER_HOST    : loaded_config.get(keys.SERVER_HOST,   "127.0.0.1"),
            keys.SERVER_PORT    : int(p) if (p := loaded_config.get(keys.SERVER_PORT, "3181")).isdigit() else 3181,
            keys.CLIENT_ID: loaded_config.get(keys.CLIENT_ID, ""),
        }
