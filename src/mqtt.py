import enum
import ssl

import paho.mqtt.client as mqtt

class _MQTTConfigKeys(enum.StrEnum):
    """
    Enum with keys for reading the configuration
    """
    USERNAME = "username"
    PASSWORD = "password"
    HOST = "host"
    PORT = "port"
    CERT_ROOT_CA = "root_ca"
    CERT_MAIN = "certificate"
    CERT_KEY_PRIVATE = "private_key"

class MQTTTaskClass:

    def get_topic(self) -> str:
        """
        :return: a constant topic string for the associated task
        """
        return ""

    def __init__(self):
        self.mqtt_manager: MQTTManager | None = None
        """
        Instance of the associated mqtt manager
        """

    def process(self, data_json: str = "") -> None:
        """
        Method for processing the integrated task
        :param data_json: the json-encoded data to use for the task
        """
        pass


class MQTTManager:
    """
    Class for providing mqtt functionality
    """

    def __init__(self, config: dict[str,str], tasks: list[MQTTTaskClass]) -> None:
        """
        Custom constructor for the class

        :param config: key-value dictionary containing configuration settings
        :param tasks: tasks to add for messaging (topics and actions)
        """
        # creating and configuring the mqtt client
        self._client = mqtt.Client(
            #client_id   = "",
            #userdata    = None,
            #protocol    = mqtt.MQTTv5
        )
        self._client.tls_set(
            ca_certs    = config.get(_MQTTConfigKeys.CERT_ROOT_CA,""),
            certfile    = config.get(_MQTTConfigKeys.CERT_MAIN,""),
            keyfile     = config.get(_MQTTConfigKeys.CERT_KEY_PRIVATE,""),
            tls_version = ssl.PROTOCOL_TLSv1_2
        )
        self._client.tls_insecure_set(False)
        self._client.username_pw_set(
            username    = config.get(_MQTTConfigKeys.USERNAME,"admin"),
            password    = config.get(_MQTTConfigKeys.PASSWORD,"")
        )

        # Saving some data to protected attributes
        self._task_dictionary = {task.get_topic(): task for task in tasks}
        self._connect_host = config.get(_MQTTConfigKeys.HOST, "")
        self._connect_port = int(p) if (p := config.get(_MQTTConfigKeys.PORT, "0")).isdigit() else 3181

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
                        topic   = task.get_topic()
                    )
                    task.mqtt_manager = self

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

                # Execute task associated to topic
                self._task_dictionary[topic].process(payload_raw)

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


    def submit(self, topic: str, data_json: str = "") -> None:
        """
        Method for sending a message to the connected mqtt server

        :param topic: topic identifier to submit on
        :param data_json: json-converted data to submit
        """
        # Checking for topic validity
        if topic not in self._task_dictionary.keys():
            print(f"ERROR (MQTTManager): Topic {topic} not registered")
            return

        # Publishing the content
        self._client.publish(
            topic   = topic,
            payload = data_json
        )