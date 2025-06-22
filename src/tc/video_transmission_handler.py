"""
    This file holds the VideoTransmission class.
"""
# Imports #
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

    def __init__(self, start_timestamp: int, video_capture_source: int = 0):
        """
        Initiating class members

        :param video_capture_source: (int) camera port
        :param start_timestamp: (int) the start timestamp for syncing.
        """
        self.port = consts.Ports.VIDEO_PORT.value
        self.video_capture_source = video_capture_source
        self.payload_type = PayloadTypes.VIDEO

        self.rtp_handle = RTPHandler(self.payload_type, start_timestamp)
        self.udp_handle = UDPClientHandler(self.port)

        self.logger = Logger("video-logger").logger

    def transmit_video(self) -> None:
        """
        transmit video using rtp
        :return: None
        """
        video_capture = VideoCapture(self.logger, self.video_capture_source)

        expected_interval = 0.02  # 20ms per packet
        prev_send_time = time.time()
        packs = 0
        timer = time.time()

        while True:
            # Capture start time

            success, frame = video_capture.get_frame()
            if success and isinstance(frame, np.ndarray):
                current_time = time.time()
                delta_time = current_time - prev_send_time

                payload = frame.tobytes()
                packets: list[bytes] = self.rtp_handle.create_packets(payload)

                if delta_time < expected_interval:
                    time.sleep(expected_interval - delta_time)

                self.udp_handle.send_packets(packets)
                time.sleep(0.005)

                packs += 1
                if time.time() - timer >= 1:
                    timer = time.time()
                    self.logger.info(f"VIDEO sent last sec: {packs}")
                    packs = 0

                prev_send_time = current_time  # Update last send timestamp
