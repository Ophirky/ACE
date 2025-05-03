"""
    Global Logging Messages for the transmitting client
"""
class ErrorMessages:
    """
    Enum to define error log messages.
    """
    OPEN_VIDEO_SOURCE = "Unable to open video source: %s"
    VIDEO_CAPTURE_INIT = "Error initializing video capture for source {source}: {error}"

    RETRIEVE_FRAME = "Failed to retrieve frame."
    GET_FRAME_FROM_SOURCE = "Error retrieving frame from video source {source}: {error}"

    RELEASE_SOURCE = "Error releasing video capture for source {source}: {error}"

    VIDEO_TRANSMISSION_ERROR = "Error while transmitting video: %s"


class SuccessMessages:
    """
    Enum to define success log messages.
    """
    RETRIEVE_FRAME = "Frame retrieved successfully."
    RELEASE_VIDEO_SOURCE = "Video source %s released successfully."
    VIDEO_CAPTURE_INIT = "Video Capture initiated successfully"

    PACKET_SENT = "Packet sent to server"
