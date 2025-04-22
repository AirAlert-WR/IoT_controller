import pyttsx3

#TODO optionally migrate to gTTS

class TextToSpeechManager:

    def __init__(self) -> None:
        """
        Custom constructor for the text-to-speech class
        """
        # creating and configuring the engine
        engine = pyttsx3.init()
        engine.getProperty("voices")

        # Setting as attributes
        self._engine = engine
        """
        INTERNAL: engine for text-to-audio
        """


    def speak(self, text: str = "") -> None:
        """
        Method for outputting a text as audio

        :param text:
        :return:
        """
        # Send text to the engine and let speaking
        self._engine.say(text)
        self._engine.runAndWait()