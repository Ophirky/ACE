"""
    This file holds all the constant variables of the transmitting client
"""
# Imports #
from enum import Enum


class CommunicationConsts(Enum):
    PORT = 5004
    HOST = '127.0.0.1'

    PAYLOAD_TYPE = 32  # uncompressed video streams
