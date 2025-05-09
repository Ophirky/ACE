"""
    This file holds all the constant variables of the transmitting client
"""
# Imports #
import logging

import pyaudio


class CommunicationConsts:
    VIDEO_PORT = 5004
    AUDIO_PORT = 5006
    HOST = '127.0.0.1'

    MAX_UDP_PAYLOAD_SIZE = 65507
    RTP_HEADER_SIZE = 12
    MAX_RTP_PAYLOAD_SIZE = MAX_UDP_PAYLOAD_SIZE - RTP_HEADER_SIZE
    RTP_EXTENSION_PROFILE_ID = b'00'
    RTP_EXTENSION_HEADER = b'0000'


class AudioCaptureConsts:
    CHANNELS = 1
    SAMPLE_RATE = 44100
    CHUNK_SIZE = 1024
    FORMAT = pyaudio.paInt32


class LoggerConsts:
    FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    LOG_LEVEL = logging.DEBUG
    LOG_DIR = r"logs/"
    LOG_FILE_EXTENSION = ".log"
