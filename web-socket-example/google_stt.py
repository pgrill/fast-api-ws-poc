import logging

from google.cloud import speech


class GoogleSTT:

    def __init__(self):
        self.client = speech.SpeechClient()

    def speech_to_text(self, content: bytes) -> str:
        try:
            audio = speech.RecognitionAudio(content=content)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
                language_code="en-US",
            )
            # Detects speech in the audio file
            response = self.client.recognize(config=config, audio=audio)
            if response and response.results:
                # TODO: Improve dealing with multiple results
                return response.results[0].alternatives[0].transcript
            return ""
        except Exception as e:
            logging.error(e)
