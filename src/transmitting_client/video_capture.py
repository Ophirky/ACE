"""
    This file holds the VideoCapture class
"""

# Imports #
import cv2
import logging
import numpy as np
import av

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
        # self.encoder = av.CodecContext.create("h265", "w")

        try:
            self.capture = cv2.VideoCapture(self.source)
            if not self.capture.isOpened():
                logging.error(ErrorMessages.OPEN_VIDEO_SOURCE % self.source)
                raise ValueError(ErrorMessages.OPEN_VIDEO_SOURCE % self.source)

            logging.info(SuccessMessages.VIDEO_CAPTURE_INIT)

        except Exception as e:
            logging.exception(ErrorMessages.VIDEO_CAPTURE_INIT.format(source=self.source, error=e))
            raise

    def get_frame(self):
        """
        Retrieves a single frame from the video source.

        :return tuple: (success, frame), where `success` is a boolean indicating if the frame was read successfully, and `frame` is the captured frame.
        """
        res_tuple: tuple[bool, np.ndarray]
        try:
            success, frame = self.capture.read()
            if success:
                logging.debug(SuccessMessages.RETRIEVE_FRAME)

                new_size = (frame.shape[1] // 2, frame.shape[0] // 2)
                img_resized = cv2.resize(frame, new_size, interpolation=cv2.INTER_AREA)
                frame = np.array(img_resized)

            else:
                logging.error(ErrorMessages.RETRIEVE_FRAME)
            return success, frame

        except Exception as e:
            logging.exception(ErrorMessages.GET_FRAME_FROM_SOURCE.format(source=self.source, error=e))
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
                logging.info(SuccessMessages.RELEASE_VIDEO_SOURCE % self.source)

        except Exception as e:
            logging.exception(ErrorMessages.RELEASE_SOURCE.format(source=self.source, error=e))

    def __del__(self) -> None:
        """
        Ensures resources are released when the instance is deleted.

        :return: None
        """
        self.release()
        logging.info(SuccessMessages.RELEASE_VIDEO_SOURCE % self.source)
