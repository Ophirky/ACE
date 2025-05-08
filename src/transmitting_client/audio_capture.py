"""
    This file contains the AudioCapture class
"""
# Imports #
from utils.consts import AudioCaptureConsts
import pyaudio
import logging


class AudioCapture:
    """ Handles real-time audio capture and streaming """

    def __init__(self):
        """
        Initializes the audio capture instance.
        """
        self.rate = AudioCaptureConsts.SAMPLE_RATE
        self.channels = AudioCaptureConsts.CHANNELS
        self.chunk_size = AudioCaptureConsts.CHUNK_SIZE

        try:
            self.audio = pyaudio.PyAudio()
            self.stream = self.audio.open(format=pyaudio.paInt16,
                                          channels=self.channels,
                                          rate=self.rate,
                                          input=True,
                                          frames_per_buffer=self.chunk_size)
            logging.info("Audio capture initialized successfully.")
        except Exception as e:
            logging.exception(f"Error initializing audio capture: {e}")
            raise

    def get_audio_chunk(self) -> bytes:
        """
        Captures and returns a single chunk of audio data.

        :return bytes: Raw audio data.
        """
        try:
            data = self.stream.read(self.chunk_size, exception_on_overflow=False)
            return data
        except Exception as e:
            logging.exception(f"Error capturing audio chunk: {e}")
            return b""

    def release(self):
        """ Cleans up resources. """
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        logging.info("Audio capture released.")
