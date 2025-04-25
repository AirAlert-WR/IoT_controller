from src.mqtttasks.base import AbstractMQTTTask

import pyttsx3

#TODO optionally migrate to aws Polly

class TextToSpeech(AbstractMQTTTask):
    """
    Class for providing text-to-speech functionality
    """

    def __init__(self) -> None:
        """
        Custom constructor for the text-to-speech class
        """
        # Call constructor of mother class
        super().__init__()

        # creating and configuring the engine
        self._engine = pyttsx3.init()

    def speak(self, text: str = "") -> None:
        """
        Method for outputting a text as audio

        :param text: the text to be converted to audio
        """
        # Send text to the engine and let speaking
        self._engine.say(text)
        #self._engine.runAndWait()

    '''
    Methods for MQTTTaskClass
    '''
    @property
    def topic(self) -> str:
        return "speech"

    def process_mqtt_task(self, data: dict) -> None:
        # Fetch the data
        text = data.get("text","")
        #language = data.get("lang_short","EN")

        # Run the engine using the data
        self.speak(text)