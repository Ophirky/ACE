"""
    This file holds the VideoCapture class
"""

# Imports #
import cv2
import logging
import numpy as np

from src.transmitting_client.utils.logging_messages import ErrorMessages, SuccessMessages


class VideoCapture:
    """
    This class handles the video capture and handling.
    """

    def __init__(self, source=0) -> None:
        """
        Initializes the video capture instance.

        :param source: (int or str): The video source, can be a camera index or a video file path.
        :return: None
        """
        self.source = source

        try:
            self.capture = cv2.VideoCapture(self.source)
            if not self.capture.isOpened():
                logging.error(ErrorMessages.OPEN_VIDEO_SOURCE.value % self.source)
                raise ValueError(ErrorMessages.OPEN_VIDEO_SOURCE.value % self.source)

            logging.info(SuccessMessages.VIDEO_CAPTURE_INIT.value)

        except Exception as e:
            logging.exception(ErrorMessages.VIDEO_CAPTURE_INIT.value.format(source=self.source, error=e))
            raise

    def get_frame(self) -> tuple[bool, np.ndarray]:
        """
        Retrieves a single frame from the video source.

        :return tuple: (success, frame), where `success` is a boolean indicating if the frame was read successfully, and `frame` is the captured frame.
        """
        res_tuple: tuple[bool, np.ndarray]
        try:
            success, frame = self.capture.read()
            if success:
                logging.debug(SuccessMessages.RETRIEVE_FRAME.value)
            else:
                logging.warning(ErrorMessages.RETRIEVE_FRAME.value)
            return success, frame

        except Exception as e:
            logging.exception(ErrorMessages.GET_FRAME_FROM_SOURCE.value.format(source=self.source, error=e))
            res_tuple = (False, np.ndarray(shape=(0, 0)))

        return res_tuple

    def release(self) -> None:
        """
        Releases the video capture resource.

        :return: None
        """
        try:
            if self.capture:
                self.capture.release()
                logging.info(SuccessMessages.RELEASE_VIDEO_SOURCE.value % self.source)

        except Exception as e:
            logging.exception(ErrorMessages.RELEASE_SOURCE.value.format(source=self.source, error=e))

    def __del__(self) -> None:
        """
        Ensures resources are released when the instance is deleted.

        :return: None
        """
        self.release()
        logging.info(SuccessMessages.RELEASE_VIDEO_SOURCE.value % self.source)
