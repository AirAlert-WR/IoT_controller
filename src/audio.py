import pyttsx3
from src.utils.mqttuser import MQTTTaskClass

#TODO optionally migrate to aws Polly

class TextToSpeechManager(MQTTTaskClass):
    """
    Class for providing text-to-speech functionality
    """

    '''
    Methods to override
    '''
    def get_topic(self) -> str:
        return "speech"

    def __init__(self) -> None:
        """
        Custom constructor for the text-to-speech class
        """
        # creating and configuring the engine
        engine = pyttsx3.init()
        voices = engine.getProperty("voices")

        # Setting as attributes
        self._engine = engine


    def speak(self, text: str = "") -> None:
        """
        Method for outputting a text as audio

        :param text:
        :return:
        """
        # Send text to the engine and let speaking
        self._engine.say(text)
        self._engine.runAndWait()