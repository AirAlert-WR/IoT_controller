import pyttsx3
import json
from src.mqtt import MQTTTaskClass

#TODO optionally migrate to aws Polly

class TextToSpeech(MQTTTaskClass):
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

    def _speak(self, text: str = "") -> None:
        """
        Method for outputting a text as audio

        :param text: the text to be converted to audio
        """
        # Send text to the engine and let speaking
        self._engine.say(text)
        #self._engine.runAndWait()

    '''
    Methods to override
    '''
    def get_topic(self) -> str:
        return "speech"

    def process(self, data_json: str = "") -> None:
        try:
            # Convert data
            data: dict[str,str] = json.loads(data_json)

            # Run the engine
            self._speak(data.get("text",""))
        except json.JSONDecodeError:
            print(f"ERROR (TextToSpeechManager): Failed to decode json.")