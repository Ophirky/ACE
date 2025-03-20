"""
Global variables
"""
from enum import Enum, auto


class ErrorMessages(Enum):
    OPEN_VIDEO_SOURCE = "Unable to open video source: %s"
    VIDEO_CAPTURE_INIT = "Error initializing video capture for source {source}: {error}"

    RETRIEVE_FRAME = "Failed to retrieve frame."
    GET_FRAME_FROM_SOURCE = "Error retrieving frame from video source {source}: {error}"

    RELEASE_SOURCE = "Error releasing video capture for source {source}: {error}"


class SuccessMessages(Enum):
    RETRIEVE_FRAME = "Frame retrieved successfully."
    RELEASE_VIDEO_SOURCE = "Video source %s released successfully."
    VIDEO_CAPTURE_INIT = "Video Capture initiated successfully"
