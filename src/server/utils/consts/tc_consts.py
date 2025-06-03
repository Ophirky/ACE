"""
    Holds the consts for the udp server
"""
from enum import Enum

from pyaudio import paInt16


# Communication Consts #
class CommunicationConsts:
    PORT = 5004
    HOST = '127.0.0.1'
    PAYLOAD_TYPE = 32  # uncompressed video streams
    BUFFER_SIZE = 65535  # Max UDP packet
    EXPECT_ANOTHER_FRAGMENT = 0
    FRAGMENT_RECEIVE_TIMEOUT = .1  # In Seconds


class Ports(Enum):
    """
    All available Ports
    """
    VIDEO_PORT = 5004
    AUDIO_PORT = 5006


# Audio Consts #
class AudioConsts:
    CHANNELS = 1
    SAMPLE_RATE = 44100
    CHUNK_SIZE = 512
    FORMAT = paInt16
