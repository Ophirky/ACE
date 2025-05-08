"""
    This file contains the AudioCapture class
"""
# Imports #
import pyaudio

from utils.consts import AudioCaptureConsts


class AudioCapture:
    """
    This class handles audio input from the client
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=AudioCaptureConsts.FORMAT, channels=AudioCaptureConsts.CHANNELS,
                                      rate=AudioCaptureConsts.SAMPLE_RATE, input=True)

    def record_chunk(self) -> bytes:
        """
        Records a frame according to the chunk size
        :return: list of frames
        """
        return self.stream.read(AudioCaptureConsts.CHUNK)

    def stop_stream(self) -> None:
        """
        Stops the audio stream
        :return: None
        """
        self.stream.stop_stream()
        self.stream.close()
