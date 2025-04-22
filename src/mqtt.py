import enum
import paho.mqtt.client as mqtt

class MQTTMessage(enum.IntEnum):
    TRIGGER_SENSOR = 0
    TRIGGER_SPEAKER = 1

class MQTTConfigKeys(enum.StrEnum):
    USERNAME = "username"
    PASSWORD = "password"
    HOST = "host"
    PORT = "port"

class MQTTManager:

    def __init__(self, config: dict[str,str]) -> None:
        """
            Custom constructor for the class
        """

        #TODO add event attributes

        '''
            MQTT client
        '''
        # creating the mqtt client
        client = mqtt.Client(
            client_id       = "",
            userdata        = None,
            protocol        = mqtt.MQTTv5
        )
        # OPTIONAL: enabling tls for secure connection
        ##client.tls_set(
        ##    tls_version    = mqtt.ssl.
        ##)
        # setting username and password for login procedure
        client.username_pw_set(
            username        = config.get(MQTTConfigKeys.USERNAME,""),
            password        = config.get(MQTTConfigKeys.PASSWORD,"")
        )

        #TODO set events and create procedures / listeners

        # setting as attributes
        self._client = client
        """
            INTERNAL: mqtt client instance
        """
        self._conn_prop = {
            MQTTConfigKeys.HOST: config.get(MQTTConfigKeys.HOST,""),
            MQTTConfigKeys.PORT: int(p)
                if (p := config.get(MQTTConfigKeys.PORT,"0")).isdigit()
                else 0
        }
        """
            INTERNAL: properties for connecting to the mqtt server
        """

    def connect(self) -> None:
        self._client.connect(
            host    = self._conn_prop[MQTTConfigKeys.HOST],
            port    = self._conn_prop[MQTTConfigKeys.PORT]
        )
