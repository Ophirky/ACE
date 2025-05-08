"""
    This file holds the VideoTransmission class.
"""
import logging
import time

import numpy as np

from rtp_handler import RTPHandler
from udp_handler import UDPClientHandler
from utils import consts
# Imports #
from utils.payload_types import PayloadTypes
from video_capture import VideoCapture


class VideoTransmission:
    """
    This class will handle the video transmission
    """

    def __init__(self, video_capture_source: int):
        """
        Initiating class members
        :param video_capture_source: (int) camera port
        """
        # TODO: remove un-needed members
        self.port = consts.CommunicationConsts.VIDEO_PORT
        self.video_capture_source = video_capture_source
        self.payload_type = PayloadTypes.VIDEO.value

        self.rtp_handle = RTPHandler(self.payload_type)
        self.udp_handle = UDPClientHandler(self.port, self.payload_type)

    def transmit_video(self) -> None:
        """
        transmit video using rtp
        :return: None
        """
        video_capture = VideoCapture(self.video_capture_source)

        while True:
            # Capture start time
            start_time = time.time()

            success, frame = video_capture.get_frame()
            if success and isinstance(frame, np.ndarray):
                payload = np.tobytes(frame)
                packets: list[bytes] = self.rtp_handle.create_packets(payload)

                did_send = self.udp_handle.send_packets(packets)

                if not did_send:
                    # TODO: Handle frame not sent
                    ...


            # Handling delta time
            delta_time = time.time() - start_time
            time.sleep(max(0.033 - delta_time, 0))  # ~30 frames per second


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,  # Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
        format="%(asctime)s - %(levelname)s - %(message)s",  # Log format
        datefmt="%Y-%m-%d %H:%M:%S"  # Date format
    )
    logging.debug("Software is awake.")

    VideoTransmission(0).transmit_video()
