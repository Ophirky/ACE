"""
    This file holds the VideoReceiveHandler class
"""
# TODO: Add Logger
# Imports #
import cv2
import numpy as np
from multiprocessing import Queue

from src.server.tc_handler.udp_handler_generic import UDPServerHandler
from src.server.utils.consts.tc_consts import Ports


class VideoReceiveHandler:
    """
    Handles real-time UDP video reception
    """

    @staticmethod
    def recv_video(video_queue: Queue) -> None:
        """
        Handles real-time UDP video reception with delta time synchronization.

        :param video_queue: (multiprocessing.Queue) queue to send the packets to
        :return: None
        """
        udp_handler = UDPServerHandler(Ports.VIDEO_PORT)

        while True:
            try:
                timestamp, frame = udp_handler.receive_rtp_message()
                array = np.frombuffer(frame, dtype=np.uint8)
                frame = np.resize(array, (240, 320, 3))

                frame = cv2.resize(frame, (640, 480))

                # Display the frame using OpenCV
                video_queue.put((timestamp, frame))

            except KeyboardInterrupt:
                break

        # Cleanup OpenCV windows after exiting the loop
        cv2.destroyAllWindows()
