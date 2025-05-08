"""
    This file holds all the constant variables of the transmitting client
"""
import pyaudio


class CommunicationConsts:
    VIDEO_PORT = 5004
    AUDIO_PORT = 5006
    HOST = '127.0.0.1'

    PAYLOAD_TYPE = 32  # uncompressed video streams
    MAX_UDP_PAYLOAD_SIZE = 65507
    RTP_HEADER_SIZE = 12
    MAX_RTP_PAYLOAD_SIZE = MAX_UDP_PAYLOAD_SIZE - RTP_HEADER_SIZE
    MAX_PACKETS_PER_FRAME = 2  # The code will break if this will be greater than 2, since a single bit is used for fragmentation sequencing
    MAX_FRAME_SIZE = MAX_RTP_PAYLOAD_SIZE * MAX_PACKETS_PER_FRAME
    RTP_EXTENSION_PROFILE_ID = b'00'
    RTP_EXTENSION_HEADER = b'0000'

class AudioCaptureConsts:
    CHANNELS = 1
    SAMPLE_RATE = 44100
    CHUNK = 1024
    FORMAT = pyaudio.paInt32
