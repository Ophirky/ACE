"""
    Global Logging Messages for the server
"""
class SuccessMessages:
    """
    Enum to define success log messages.
    """
    SERVER_LISTENING = "Server is now listening on {}:{}"
    PACKET_SENT = "RTP packet successfully sent to the server."
    PACKET_RECEIVED = "RTP packet successfully received by the server."
    VIDEO_STREAM_STARTED = "Video streaming has started successfully."
    CONNECTION_ESTABLISHED = "Connection successfully established with {}:{}"


class ErrorMessages:
    """
    Enum to define error log messages.
    """
    VIDEO_TRANSMISSION_ERROR = "An error occurred while transmitting video: {}"
    VIDEO_RECEIVING_ERROR = "An error occurred while receiving video: {}"
    DECODE_PACKET_ERROR = "Failed to decode the RTP packet: {}"
    PAYLOAD_EXTRACTION_ERROR = "Error extracting payload from the RTP packet: {}"
    SOCKET_CREATION_ERROR = "Error creating the UDP socket: {}"
    CONNECTION_ERROR = "Error while establishing connection to the server: {}"
    VIDEO_STREAM_ERROR = "Error occurred during video streaming: {}"
