import logging
from typing import List

from google.cloud import speech


class GoogleSTT:

    def __init__(self):
        self.client = speech.SpeechClient()

    def speech_to_text(self, content: List[bytes]) -> str:
        try:
            def generator():
                for chunk in content:
                    yield speech.StreamingRecognizeRequest(audio_content=chunk)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,
                sample_rate_hertz=48000,
                language_code="en-US",
            )
            streaming_config = speech.StreamingRecognitionConfig(config=config)
            # Detects speech in the audio file
            responses = self.client.streaming_recognize(
                config=streaming_config,
                requests=generator(),
            )
            for response in responses:
                return response.results[0].alternatives[0].transcript
        except Exception as e:
            logging.error(e)
