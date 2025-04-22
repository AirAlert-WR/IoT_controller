import pyttsx3

#TODO optionally migrate to gTTS

class TextToSpeechManager:

    def __init__(self):
        """
            Custom constructor for the text-to-speech class
        """
        self._engine = pyttsx3.init()
        """
            INTERNAL: engine for text-to-audio
        """

        # Configuring the engine



