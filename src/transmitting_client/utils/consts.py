"""
    This file holds all the constant variables of the transmitting client
"""


# Imports #


class CommunicationConsts:
    PORT = 5004
    HOST = '127.0.0.1'

    PAYLOAD_TYPE = 32  # uncompressed video streams
    MAX_UDP_PAYLOAD_SIZE = 65507
    RTP_HEADER_SIZE = 12
    MAX_RTP_PAYLOAD_SIZE = MAX_UDP_PAYLOAD_SIZE - RTP_HEADER_SIZE
    MAX_PACKETS_PER_FRAME = 2  # The code will break if this will be greater than 2, since a single bit is used for fragmentation sequencing
    MAX_FRAME_SIZE = MAX_RTP_PAYLOAD_SIZE * MAX_PACKETS_PER_FRAME
    RTP_EXTENSION_PROFILE_ID = b'00'
    RTP_EXTENSION_HEADER = b'0000'
