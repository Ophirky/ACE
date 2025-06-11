"""
    This file holds the Transcriptor class.
"""
# Imports #
import json

from vosk import Model, KaldiRecognizer
from src.server.transcriptor.transcriptor_consts import TranscriptorConsts

class Transcriptor:
    """
    This class handles the live transcription of the audio
    """
    def __init__(self) -> None:
        """
        Initializes the Transcriptor class

        :return: None
        """
        self.logger = ""
        self._model = Model(TranscriptorConsts.MODEL_PATH)
        self._recognizer = KaldiRecognizer(self._model, TranscriptorConsts.SAMPLE_RATE_HZ)
    
    def transcript_chunk(self, chunk: bytes) -> str:
        """
        Transcripts audio chunks received.

        :param chunk: (bytes) The audio chunk received
        :return str: Transcribed audio chunk.
        """
        if self._recognizer.AcceptWaveform(chunk):
            text = json.loads(self._recognizer.Result())["text"]
        else:
            text = json.loads(self._recognizer.PartialResult())["partial"]
        
        t = text.split(' ')
        return text if len(t) <= 7 else " ".join(t[len(t)-7:])


