import enum
import json
from typing import Callable

import paho.mqtt.client as mqtt

class MQTTTopic(enum.StrEnum):
    """
    Enum with keys for subscribing to mqtt topics
    """
    TRIGGER_SENSOR = "sensor"
    TRIGGER_SPEECH = "speech"

class MQTTConfigKeys(enum.StrEnum):
    """
    Enum with keys for reading the configuration
    """
    USERNAME = "username"
    PASSWORD = "password"
    HOST = "host"
    PORT = "port"

class MQTTManager:
    """
    Class for providing mqtt functionality
    """

    def __init__(self, config: dict[str,str]) -> None:
        """
        Custom constructor for the class

        :param config: key-value dictionary containing configuration settings
        """

        # creating and configuring the mqtt client
        client = mqtt.Client(
            client_id       = "",
            userdata        = None,
            protocol        = mqtt.MQTTv5
        )
        client.tls_set(
            tls_version    = 2
        )
        client.username_pw_set(
            username        = config.get(MQTTConfigKeys.USERNAME,""),
            password        = config.get(MQTTConfigKeys.PASSWORD,"")
        )

        # Set listeners for the internal client
        client.on_connect = self.__on_client_connect

        #TODO set events and create procedures / listeners

        # setting as attributes
        self.on_message: Callable[[MQTTTopic, dict[str, any]], None] = lambda topic, data: None
        """
        PUBLIC: event handler for external processing of received messages
        """
        self._client = client
        """
        INTERNAL: mqtt client instance
        """

        # Setting an internal lambda for making the connection task more compact
        self.__internal_connect = lambda: self._client.connect(
            host    = config.get(MQTTConfigKeys.HOST, ""),
            port    = int(p)
            if (p := config.get(MQTTConfigKeys.PORT, "0")).isdigit()
            else 0
        )

    '''
    Public methods
    '''
    def connect(self) -> None:
        """
        Method for attempting a server connection.
        """
        # Calling the internal method
        self.__internal_connect()
        # Starting the thread
        self._client.loop_start()


    def disconnect(self) -> None:
        """
        Method for disconnecting from the client
        """
        self._client.disconnect()


    def submit(self, topic: MQTTTopic, data = dict[str,any]) -> None:
        """
        Method for sending a message to the connected mqtt server

        :param topic: topic identifier to submit on
        :param data: data to submit on
        """
        # Converting data to json
        data_json = json.dumps(data)
        # Publishing the content
        self._client.publish(
            topic   = topic,
            payload = data_json
        )

    '''
    Internal methods for the mqtt client
    '''
    def __on_client_connect(self, client: mqtt.Client, userdata, flags, rc: int):
        """
        INTERNAL: called when client is connecting
        """
        if rc == 0:
            # print success
            print("Connection established")

            # Subscribe to all topics
            for topic in MQTTTopic:
                client.subscribe(
                    topic   = topic
                )

        else:
            # else print error
            print(f"ERROR: Connection not successful, Code {rc}")
