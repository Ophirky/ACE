"""
    This file holds the VideoTransmission class.
"""
# Imports #
import logging
import time

import numpy as np

from rtp_handler import RTPHandler
from udp_handler import UDPClientHandler
from utils import consts
from utils.payload_types import PayloadTypes
from video_capture import VideoCapture
from utils.logger import Logger


class VideoTransmission:
    """
    Bundles video handlers and handles transmission
    """

    def __init__(self, video_capture_source: int):
        """
        Initiating class members

        :param video_capture_source: (int) camera port
        """
        # TODO: remove un-needed members
        self.port = consts.Ports.VIDEO_PORT.value
        self.video_capture_source = video_capture_source
        self.payload_type = PayloadTypes.VIDEO

        self.rtp_handle = RTPHandler(self.payload_type)
        self.udp_handle = UDPClientHandler(self.port)

        self.logger = Logger("video-logger").logger

    def transmit_video(self) -> None:
        """
        transmit video using rtp
        :return: None
        """
        video_capture = VideoCapture(self.logger, self.video_capture_source)

        while True:
            # Capture start time
            start_time = time.time()

            success, frame = video_capture.get_frame()
            if success and isinstance(frame, np.ndarray):
                payload = frame.tobytes()
                packets: list[bytes] = self.rtp_handle.create_packets(payload)

                did_send = self.udp_handle.send_packets(packets)

                if not did_send:
                    # TODO: Handle frame not sent
                    ...

            # Handling delta time
            delta_time = time.time() - start_time
            time.sleep(max(0.033 - delta_time, 0))  # ~30 frames per second


if __name__ == '__main__':
    VideoTransmission(0).transmit_video()
