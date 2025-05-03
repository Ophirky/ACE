"""
    Holds the consts for the udp server
"""
class CommunicationConsts:
    PORT = 5004
    HOST = '127.0.0.1'
    PAYLOAD_TYPE = 32  # uncompressed video streams
    BUFFER_SIZE = 65535  # Max UDP packet
    EXPECT_ANOTHER_FRAGMENT = 0
    FRAGMENT_RECEIVE_TIMEOUT = .1  # In Seconds
