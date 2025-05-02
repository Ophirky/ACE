"""
    Holds the consts for the udp server
"""
# Imports #
from enum import Enum


class CommunicationConsts(Enum):
    PORT = 5004
    HOST = '127.0.0.1'
    PAYLOAD_TYPE = 32  # uncompressed video streams
    BUFFER_SIZE = 65535  # Max UDP packet
